from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta



from account.models import Account,RefferalProfile

from .models import Transactions,Notification,Investments,Packages
from .forms import UserUpdateForm,PasswordChangeForm
from . import utils

D =  'deposite'
W = "withdraw"




@login_required
def dashbaord_view(request):
    investment = get_object_or_404(Investments, user=request.user)
    if investment.is_complete == True:
        messages.success(request, f'INVESTMENT HAS BEEN COMPLETED')
    elif investment.status == "inactive":
        messages.success(request, f'YOU MUST INVEST BEFORE YOU CAN START RECIEVING REFERRAL BONUS')
    return render(request,'users/dashboard.html',{"investment":investment})



@login_required
def withdrawal_view(request):
    if request.POST:
        user = request.user
        amount = int(request.POST.get('amount'))
        coin_tpye = request.POST.get('coin')
        wallet_address = request.POST.get('wallet_address')
        if amount > user.balance:
            messages.success(request, ('Inssuficient Funds'))
            return redirect("withdraw")
        else:
            Transactions.objects.create(user= user, amount=amount,coin_tpye=coin_tpye,trans_type=W,wallet_address=wallet_address)
            user.balance -= amount
            user.save()
            messages.success(request, ('Your Withdrawal Has Been Made, You Will Be Notify Once It Has Been Approved'))
            return redirect("withdraw")
    else:
        return render(request,'users/withdraw.html')



@login_required
def deposit_view(request):
    if request.POST:
        user = request.user
        amount = request.POST.get('amount')
        coin_tpye = request.POST.get('coin')
        Transactions.objects.create(user= user, amount=amount,coin_tpye=coin_tpye,trans_type=D)
        messages.success(request, ('Your Deposit Has Been Made, You Will Be Notify Once It Has Been Approved'))
        return redirect("deposit")
    else:
        return render(request,'users/deposit.html')



@login_required
def settings_view(request):
    user = request.user
    if request.POST:
        submit = request.POST.get('submit')
        if submit == 'Update Profile':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, ('YOUR ACCOUNT HAS BEEN UPDATED'))
                return redirect("settings")
        else:
            messages.info(request, f'Unknown error Occured')
            return redirect('settings')
    else:
         
        u_form = UserUpdateForm(instance=user)
        #p_form =  PasswordChangeForm(initial={'user_id': user.id})
    return render(request,'users/settings.html',{'u_form':u_form})


@login_required
def change_password_view(request):
    user = request.user
    if request.POST:
        submit = request.POST.get('submit')
        if submit == 'Change Password':
            p_form = PasswordChangeForm(request.POST,instance=user)
            if p_form.is_valid():
                password1 = p_form.cleaned_data['password1']
                user.set_password(password1)
                user.save()
                messages.info(request, f'Password Change')
                return redirect('change_password')
        else:
            messages.info(request, f'Unknown error Occured')
            return redirect('change_password')
    else:
        p_form =  PasswordChangeForm(initial={'user_id': user.id})
    return render(request,'users/change_password.html',{'p_form':p_form})












@login_required
def history_view(request):
    transactions = Transactions.objects.filter(user=request.user).order_by('-date')
    return render(request,'users/history.html',{"transactions":transactions})


@login_required
def notification_view(request):
    notification = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request,'users/notification.html',{'notification':notification})



@login_required
def create_investment_view(request):
    packages = Packages.objects.all()
    user = request.user
    investment = get_object_or_404(Investments,user=user)
    if request.POST:
        package_id =  int(request.POST.get('package'))
        amount = int(request.POST.get('amount'))
        package = get_object_or_404(Packages, pk=package_id)
        if user.deposite_balance >=  amount:
            if amount not in range(package.min_amount ,package.max_amount):
                messages.success(request, (f'Input Amount Between Your Selected Plans Price'))
                return redirect("create_investment")
            investment.end_date = utils.get_deadline(package.hours)
            investment.start_date = timezone.now()
            investment.status = 'active'
            investment.amount_invested = amount
            investment.package = package
            investment.is_complete = False 
            user.deposite_balance -=  amount
            user.total_amount_invested +=  amount
            user.total_investement_count += 1
            user.save()
            investment.save()
            messages.success(request, ('YOUR INVESTMENT HAS BEEN ACTIVATED'))
            return redirect("dashboard")
        else:
            messages.success(request, ('INSUFFICIENT FUNDS,PLEASE DEPOSIT'))
            return redirect("create_investment")
    return render(request,'users/create_investment.html',{'packages':packages})






def end_user_investment_view(request):
    if request.POST:
        user = request.user
        investment = get_object_or_404(Investments, user=user)
        investment.status = "completed"
        investment.amount_earn += utils.earnings(investment.amount_invested,investment.package.percent)
        investment.is_complete = True 
        user.balance += utils.earnings(investment.amount_invested,investment.package.percent)
        user.save()
        investment.save()
        Notification.objects.create(user=user,title="Investment Has Been Completed", body=f" YOUR INVESTMENT OF ${investment.amount_invested} HAS BEEN COMPLETED YOU CAN NOW RENEW OR UPGRADE YOUR PLAN")
        return JsonResponse({"msg":"Account Credited"})
    else:
        return JsonResponse({"msg":"Get Request Not Accepted"})





@login_required
def referral_view(request):
    user = request.user
    account = RefferalProfile.objects.get(user=user)
    myrecs = account.recom_profies()
    return render(request,'users/referral.html',{'myrecs':myrecs})