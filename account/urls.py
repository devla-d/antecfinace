from django.urls import path
from . import views





urlpatterns = [ 
    
    path('sign-in/',views.loginpage,name="login"),
    path('sign-up/',views.registerpage,name="register"),
    path('sign-out/',views.logout_view,name="logout"),
    path('activate/<uidb64>/<token>/', views.account_activate_view, name='activate'),
]
