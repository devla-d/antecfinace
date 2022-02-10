from django.contrib import admin

from .models import Transactions,Notification,Investments,Packages



admin.site.register(Transactions)
admin.site.register(Notification)
admin.site.register(Investments)
admin.site.register(Packages)