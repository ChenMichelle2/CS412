from django.shortcuts import render, redirect
import time

# Create your views here.

def order(request):
  '''Show the order form'''

  template_name = "restaurant/order.html"
  context={
    'current_time': time.ctime(),
  }
  return render(request,template_name,context)


def submit(request):
  '''
  Handle the form submission  
  Reead the form data from the request,
  and send it back to a template
  '''

  template_name ='restaurant/confirmation.html'
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
      'current_time': time.ctime(),
    }

    return render(request,template_name,context)
  
  ## handel GET request on this URL
  ##template_name = "formdata/form.html"
  ##return render(request,template_name)

  ##a better yet solution: redirect to the correct URL:
  return redirect("show_form")

def main(request):
  '''shows the main page of the restaurant'''

  template_name = "restaurant/main.html"
  image_1 = "https://lh5.googleusercontent.com/p/AF1QipOLnrLyj7vS9jDBhQsfKSFqL7rfOc0Yf4yh87So=w1600-h1000-k-no"
  context = {
        "current_time" : time.ctime(),
        "pic": image_1
  }
  return render(request,template_name,context)