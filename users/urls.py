from django.urls import path
from . import views





urlpatterns = [ 
    
    path('wallet/',views.dashbaord_view,name="dashboard"),
    path('withdraw-funds/',views.withdrawal_view,name="withdraw"),
    path('fund-account/',views.deposit_view,name="deposit"),
    path('my-account-settings/',views.settings_view,name="settings"),
    path('update-password/',views.change_password_view,name="change_password"),
    path('account-logs/',views.history_view,name="history"),
    path('notifications/',views.notification_view,name="notifications"),
    path('create-investment/',views.create_investment_view,name="create_investment"),
    path('credit-user-investment/', views.end_user_investment_view, name="end_user_investment_view"),
    path('referrals/',views.referral_view,name="referrals"),

    
]
