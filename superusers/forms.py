from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField



from account.models import Account






class UserChangeForm(forms.ModelForm):
    """fullname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'FULLNAME'
            }
        ),
        label = 'Fullname',
        required=True
    )
    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control ',
                'placeholder':"Email"
            }
        ),
        label = 'Email',
        required=True
    )
    username = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control ',
                'placeholder':"Username"
            }
        ),
        label = 'Username',
        required=True
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control ',
                'placeholder':'PHONE'
            }
        ),
        label = "Phone",
         required=True
    )
    country = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'Country'
            }
        ),
        label = 'Country',
        required=True
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'City'
            }
        ),
        label = 'City',
        required=True
    )
    state = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'State'
            }
        ),
        label = 'State',
        required=True
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'ADDRESS'
            }
        ),
        label = 'ADDRESS',
        required=True
    )
 
    zipcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'zipcode'
            }
        ),
        label = 'Zipcode',
        required=True
    )
    gender = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control ',
                "placeholder":'Gender'
            }
        ),
        label = 'Gender',
        required=True
    )
    password = ReadOnlyPasswordHashField()"""
    #password = ReadOnlyPasswordHashField()
 
    class Meta:
        model = Account
        fields = ('email','username','phone','country','city','state','address','zipcode','gender','balance','deposite_balance','total_amount_invested','total_investement_count','withdraw_total','is_email_verifield','last_login', 'date_joined')
        #fields = "__all__"



