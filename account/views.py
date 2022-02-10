from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import  messages
from django.http import JsonResponse
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template






from .models import Account,RefferalProfile
from .forms import UserCreationForm,LoginForm



EMAIL_ADMIN = "worldcryptocurrencies01@gmail.com"

def calculate_perc():
    return 100

def loginpage(request):
    return render(request,'auth/login.html')



def registerpage(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = '@'+str(request.POST.get('username'))
            instance = form.save(commit=False)
            instance.username = username
            instance.firstname = str(request.POST.get('firstname'))
            instance.lastname = str(request.POST.get('lastname'))
            instance.is_active = False
            instance.save()
            

            if request.POST.get('refferd_by'):
                refferd_by_id = int(request.POST.get('refferd_by'))
                print(refferd_by_id)
                try:
                    refferd_by_user = Account.objects.get(pk=refferd_by_id)
                    new_user_ref =  RefferalProfile.objects.create(user=instance)
                    new_user_ref.recommended_by = refferd_by_user
                    new_user_ref.save()
                    old_user_ref = RefferalProfile.objects.get(user =refferd_by_user)
                    old_user_ref.user.refferal += 1
                    old_user_ref.user.bonus += calculate_perc()
                    old_user_ref.user.balance += calculate_perc()
                    old_user_ref.save()
                    old_user_ref.user.save()
                except:
                    messages.info(request, f'Something went Wrong')
                    return redirect('register')
            else:
                RefferalProfile.objects.create(user=instance)






            current_site = get_current_site(request)
            subject = '[Antecfinance]Confirm Your Email Address'
            context = {
                'user': instance,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': default_token_generator.make_token(instance),
                }
            message = get_template("auth/account_activation_email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=EMAIL_ADMIN,
                to=[instance.email],
                reply_to=[EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            
            messages.success(request, ('Please check your mail box for confirmation email'))
            return redirect("register")
    else:
        form = UserCreationForm()
    if request.GET.get('ref-code'):
        refferd_by = request.GET.get('ref-code')
        return render(request, 'auth/register.html',{"form":form , "refferd_by" : refferd_by})
    else:
        return render(request, 'auth/register.html',{"form":form})














def account_activate_view(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verifield = True
        user.save()
        login(request, user)
        messages.success(request, ('Please Complete Your Account Setup'))
        return redirect('settings')
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('register')




def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    destination = get_redirect_if_exists(request) 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            destination = request.POST.get('destination')
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                if destination:
                    return redirect(destination)
                else:
                    return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html',{"form":form,"destination":destination})



def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def logout_view(request):
    logout(request)
    return redirect('login')



