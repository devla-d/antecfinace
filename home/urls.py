from django.urls import path
from . import views





urlpatterns = [ 
    path('',views.homepage,name="homepage"),
    path('about/',views.aboutpage,name="aboutpage"),
    path('contact/',views.contactpage,name="contactpage"),
    path('pricing/',views.pricingpage,name="pricingpage"),
    path('services/',views.servicespage,name="servicespage"),
]
