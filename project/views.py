from django.views.generic import *
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import *
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .forms import *



# Create your views here.
class ShowAllDragons(ListView):
    '''the view to show all Profiles'''
    model = Dragon #the model to display
    template_name = 'project/all_dragons.html'
    context_object_name = 'dragons' # how to find the data in the template file
    def get_context_data(self, **kwargs):
        # Get the default context data from the ListView
        context = super().get_context_data(**kwargs)

        return context
    def get_queryset(self):
        queryset = super().get_queryset()

    # Get filters from request.GET
        name = self.request.GET.get('name')
        available = self.request.GET.get('available')

    # Apply filters
        if name:
            queryset = queryset.filter(name__icontains=name)
        if available in ['true', 'false']:
            queryset = queryset.filter(available=(available == 'true'))

        return queryset
  
class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/user_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile_project
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['favorite_dragon'] = FavoriteDragon.objects.get(profile=self.get_object())
        except FavoriteDragon.DoesNotExist:
            context['favorite_dragon'] = None
        context['wishlist'] = Wishlist.objects.filter(profile=self.get_object())
        return context
    
class CustomLogoutView(LogoutView):
    """Custom Logout View to redirect to the All Dragons page"""
    next_page = '../show_all_dragons/'  # Redirect to the All Dragons page
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
  
class CustomLoginView(FormView):
    template_name = 'project/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)  
    def get_success_url(self):
        # Redirect to Show All Dragons page
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        return next_url if next_url else '/project/show_all_dragons/' 
    
def CreateUserAndProfile(request):
    if request.method == 'POST':
        # Bind the forms with the submitted data
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user form
            user = user_form.save()

            # Save the profile form and link it to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('/project/login/')  # Redirect to the profile page after creation

    else:
        # Instantiate empty forms for a GET request
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'project/create_user_and_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

class AddToWishlistView(LoginRequiredMixin, FormView):
    template_name = 'project/add_wishlist.html'
    form_class = AddWishlist
    success_url = '../me'  # Redirect to profile
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude dragons already in the user's wishlist
        profile = self.request.user.profile_project
        form.fields['dragon'].queryset = Dragon.objects.exclude(
            id__in=profile.wishlists.values_list('dragon_id', flat=True)
        )
        return form

    def form_valid(self, form):
        # Save the wishlist item with the user's profile
        wishlist_item = form.save(commit=False)
        wishlist_item.profile = self.request.user.profile_project
        wishlist_item.save()
        return super().form_valid(form)
    
class EditFav(LoginRequiredMixin, FormView):
    template_name = 'project/fav_drag.html'
    form_class = AddFav
    success_url = '../me'

    def get_initial(self):
        # Prepopulate the form with the current favorite dragon if it exists
        profile = self.request.user.profile_project
        favorite_dragon = getattr(profile, 'favorite_dragon', None)
        if favorite_dragon:
            return {'dragon': favorite_dragon.dragon.id}
        return {}

    def form_valid(self, form):
        profile = self.request.user.profile_project
        # Replace or create the favorite dragon for the profile
        FavoriteDragon.objects.update_or_create(
            profile=profile,
            defaults={'dragon': form.cleaned_data['dragon']}
        )
        return super().form_valid(form)
    
class RemoveFromWishlistView(LoginRequiredMixin, FormView):
    template_name = 'project/remove_wishlist.html'
    form_class = RemoveFromWishlistForm
    success_url = '../me'  # Redirect to profile page after removal

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Include only dragons in the user's wishlist
        profile = self.request.user.profile_project
        form.fields['dragon'].queryset = Dragon.objects.filter(
            id__in=profile.wishlists.values_list('dragon_id', flat=True)
        )
        return form

    def form_valid(self, form):
        # Remove the selected dragon from the user's wishlist
        profile = self.request.user.profile_project
        dragon = form.cleaned_data['dragon']

        # Delete the wishlist item
        Wishlist.objects.filter(profile=profile, dragon=dragon).delete()
        return super().form_valid(form)
    
class AboutView(TemplateView):
    template_name = 'project/about.html'

class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = 'project/update_profile.html'
    form_class = UpdateProfileDragonForm
    success_url = '../me/'  # Redirect after successful update

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Prepopulate the form with the current profile data
        profile = self.request.user.profile_project
        form.instance = profile
        return form

    def form_valid(self, form):
        # Save the updated profile data
        form.save()
        return super().form_valid(form)
    