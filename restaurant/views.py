from django.shortcuts import render, redirect
import time
import random

# Create your views here.
list_items = ["Crab Ragoons", "Beef Lo Mein", "Vegetable Lo Mein", "Roast Duck"]
prices = [7,10,9,20]
random_num= random.randint(0,3)
new_list = []
new_price =[]
daily_price = 0
for i in list_items:
  if i != list_items[random_num]:
       new_list.append(i)
for i in range(0,4):
  if i == random_num:
      daily_price = 5
  else:
      new_price.append(prices[i])
daily_special = list_items[random_num]
def main(request):
  '''shows the main page of the restaurant'''

  template_name = "restaurant/main.html"
  image_1 = "https://lh5.googleusercontent.com/p/AF1QipOLnrLyj7vS9jDBhQsfKSFqL7rfOc0Yf4yh87So=w1600-h1000-k-no"
  context = {
        "current_time" : time.ctime(),
        "pic": image_1
  }
  return render(request,template_name,context)

def order(request):
  '''Show the order form'''

  template_name = "restaurant/order.html"

  context={
    'current_time': time.ctime(),
    'daily_special':daily_special,
    'new_list1': new_list[0],
    'new_list1': new_list[1],
    'full_list': new_list,
    'full_prices': new_price,
    'daily_price': daily_price,
    'list_1': new_list[0],
    'price_1':new_price[0],
    'list_2': new_list[1],
    'price_2':new_price[1],
    'list_3': new_list[2],
    'price_3':new_price[2],
  }

  return render(request,template_name,context,)


def confirmation(request):
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
    ordered_items = []
    total_price = 0

    ordered_items_raw = request.POST.getlist('ordered_items')

    for item in ordered_items_raw:
            item_name, item_price = item.split(',')
            ordered_items.append(item_name)
            total_price += float(item_price)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    current_time = time.time()  # Get the current time in seconds
    ready_in_seconds = random.randint(30 * 60, 60 * 60)  # Random seconds between 30 and 60 minutes
    ready_time = current_time + ready_in_seconds 
    ready_time_formatted = time.ctime(ready_time)
    context = {
            'name': name,
            'phone': phone,
            'email': email,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'current_time': time.ctime(),
            'ready_time': ready_time_formatted,
        }

    return render(request,template_name,context)
  
  ## handel GET request on this URL
  ##template_name = "formdata/form.html"
  ##return render(request,template_name)

  ##a better yet solution: redirect to the correct URL:
  return redirect("order")

