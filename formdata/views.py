from django.shortcuts import render, redirect


# Create your views here.

def show_form(request):
  '''Show the contact form'''

  template_name = "formdata/form.html"
  return render(request,template_name)

def submit(request):
  '''
  Handle the form submission  
  Reead the form data from the request,
  and send it back to a template
  '''

  template_name = 'formdata/confirmation.html'
  print(request)

  #check that we have a POST request
  if request.POST:

    print(request.POST)
    #read the form data into python variables
    name = request.POST['name']
    favorite_color = request.POST['favorite_color']
    #package the form data up as contect variables for the template


    context ={
      'name': name,
      'favorite_color':favorite_color,
    }

    return render(request,template_name,context)
  
  ## handel GET request on this URL
  ##template_name = "formdata/form.html"
  ##return render(request,template_name)

  ##a better yet solution: redirect to the correct URL:
  return redirect("show_form")