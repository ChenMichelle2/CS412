## hw/views.py
## description: write view functions to handle URL requests for the hw app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
# def home(request):
#     '''Handle the main URL for the hw app.'''

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''
#     # create and return a response to the client:
#     return HttpResponse(response_text)
list_of_pics = ["https://m.media-amazon.com/images/M/MV5BMzdjMWUzMGEtMzU1Ny00YmQzLWE2ZjItZDBiZmZlMzk2ZTM2XkEyXkFqcGc@._V1_.jpg",
                    "https://yt3.googleusercontent.com/FFnXJb38aoIO9zvfz9DdC4kQEZIubwr-HHkD-9V7klqundQvIS8Su3mrRQCKi5dtRo7Wbz8Wcw=s900-c-k-c0x00ffffff-no-rj",
                    "https://img1.wsimg.com/isteam/ip/175fa811-14be-4397-ab26-16f54c04d81d/0BBAEB6F-C01A-4402-82EB-E8602115EDE6.jpeg/:/cr=t:0%25,l:0%25,w:100%25,h:100%25/rs=w:400,cg:true",
                    "https://kpopping.com/documents/84/0/231120-JUNGKOOK-GOLDEN-LIVE-ON-STAGE-documents-1.jpeg?v=d965b"]
    
list_of_quotes = ["“I realized that I should think twice before I do anything and not forget where I am, no matter what situation I may be in.”",
                      "“Don’t lose the people beside you because of your mistakes and wrongs. And live [your life] to the fullest.”",
                      "“Without anger or sadness, you won’t be able to feel true happiness.”",
                      "“There’s no knowing what will come, but hard work will get us somewhere.“"]
def quote(request):
    '''
    Function to handle the URL request for /hw (home page).
    Delegate rendering to the template hw/home.html.
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'
    
    # create a dictionary of context variables for the template:
    context = {
        
        "current_time" : time.ctime(),
        "letter1" : chr(random.randint(65,90)), # a letter from A ... Z
        "letter2" : chr(random.randint(65,90)), # a letter from A ... Z
        "number" : random.randint(1,10), # number frmo 1 to 10
        "current_image" : list_of_pics[random.randint(0,3)],
        "current_quote" : list_of_quotes[random.randint(0,3)],
    }
    

    # delegate rendering work to the template
    return render(request, template_name, context)


def about(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'
    context = {
        "current_time" : time.ctime(),
        "pic_1": list_of_pics[0],
        "pic_2": list_of_pics[1],
        "pic_3": list_of_pics[2],
        "pic_4": list_of_pics[3],
        "quote_1": list_of_quotes[0],
        "quote_2": list_of_quotes[1],
        "quote_3": list_of_quotes[2],
        "quote_4": list_of_quotes[3]
    }
    return render(request,template_name, context)