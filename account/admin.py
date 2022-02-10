from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group



from .models import Account,RefferalProfile

from . forms import UserChangeForm, UserCreationForm





class UserAdmin(BaseUserAdmin):
  form = UserChangeForm
  fieldsets = (
      (None, {'fields': ('email', 'password', )}),
      (_('Personal info'), {'fields': ('username','country','gender','state','zipcode','city','address','date_of_birth','phone')}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_email_verifield' )}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {'fields': ( 'balance','withdraw_total','deposite_balance','total_amount_invested','total_investement_count')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('email', 'password1', 'password2'),
      }),
  )
  list_display = [ 'username', ]
  search_fields = ('email', 'username' )
  ordering = ('id', )



# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
admin.site.register(RefferalProfile)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)