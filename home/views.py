from django.shortcuts import render

# Create your views here.



def homepage(request):
    return render(request, 'index.html')




def aboutpage(request):
    return render(request, 'about.html')


def contactpage(request):
    return render(request, 'contact.html')

def pricingpage(request):
    return render(request, 'pricing.html')

def servicespage(request):
    return render(request, 'services.html')