from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth  import login,authenticate,logout
from .models import Account





class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Firstname'
            }
        ),
        label = 'Firstname',
        required=True
    )
    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Lastname'
            }
        ),
        label = 'Lastname',
        required=True
    )
    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder':"Email"
            }
        ),
        label = 'Email',
        required=True
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder':'PHONE'
            }
        ),
        label = "PHONE",
         required=True
    )
    password1 = forms.CharField( max_length=30, min_length=6,label='Password', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}))
    #password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': "CONFIRM PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ('firstname','lastname',"username",'email','phone','password1')


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]









class UserActivateForm(forms.ModelForm):

    country = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Country'
            }
        ),
        label = '',
        required=True
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'City'
            }
        ),
        label = '',
        required=True
    )
    state = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ZIPCODE'
            }
        ),
        label = '',
        required=True
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ADDRESS'
            }
        ),
        label = '',
        required=True
    )
 
    zipcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'zipcode'
            }
        ),
        label = '',
        required=True
    )
    gender = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Gender'
            }
        ),
        label = '',
        required=True
    )

 


    class Meta:
        model = Account
        fields = ['country','city','state','address','zipcode','gender']




class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                "placeholder":'EMAIL'
            }
        ),
        label = 'Email',
        required=True
    )
    password = forms.CharField( max_length=30, min_length=4,label='Password', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ['email','password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password =  self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('Invalid Credentials Note : Make Sure Your Email Address Is Verified')

