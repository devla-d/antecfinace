from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import  messages
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string

 


from account.models import Account
from users.models import Transactions,Notification,Investments,Packages

from .forms import  UserChangeForm
from .decorators import manager_required

EMAIL_ADMIN = "worldcryptocurrencies01@gmail.com"
D =  'deposite'
W = "withdraw"

@manager_required
def dashboard_view(request):
    total_earnings = 0
    investments = Investments.objects.filter(status="active")
    for invest in investments:
        total_earnings += invest.amount_invested
    context = {
        "amount_invested" : total_earnings,
        "users" : Account.objects.all().count(),
        "pending_payment": Transactions.objects.filter(status="pending").count()
    }
    return render(request, 'superuser/index.html',context)



@manager_required
def users_view(request):
    users = Account.objects.all().order_by("-date_joined")
    return render(request, 'superuser/users.html',{'users':users})




@manager_required
def user_detail_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.POST:
        form = UserChangeForm(request.POST,instance=account)
        if form.is_valid():
            form.save()
            messages.info(request,("Account updated"))
            return redirect(f'/user/{account.pk}/')
    else:
        form = UserChangeForm(instance=account)
    return render(request, 'superuser/user_detail.html',{"account":account,"form":form})




@manager_required
def deposit_view(request):
    deposits = Transactions.objects.filter(trans_type=D).order_by('-date')
    return render(request, 'superuser/deposits.html',{"deposits":deposits})



@manager_required
def deposit_detail_view(request, pk):
    deposit = get_object_or_404(Transactions,pk=pk)
    if request.POST:
        submit = request.POST.get('submit')
        if submit == "Approve":
            deposit.status = 'approved'
            deposit.user.deposite_balance += deposit.amount
            subject = "Transaction Approved"
            message = render_to_string('superuser/deposite-email.html', {
                'user': deposit.user,
                'date': timezone.now(),
                'amount': deposit.amount,
                'status': "Approved",
            })
            deposit.user.save()
            deposit.save()
            Notification.objects.create(user=deposit.user,title="Transaction Approved", body=f" YOUR DEPOSIT OF ${deposit.amount} HAS BEEN APPROVED YOU CAN NOW BUY A PLAN")
            deposit.user.email_user(subject, message)
            messages.success(request, ('Transaction Approved'))
            return redirect(f'/superuser/{deposit.id}/')
        elif submit == "Decline":
            deposit.status = 'declined'
            subject = "Transaction Declined"
            message = render_to_string('superuser/deposite-email.html', {
                'user': deposit.user,
                'date': timezone.now(),
                'amount': deposit.amount,
                'status': "Declined",
            })
            Notification.objects.create(user=deposit.user,title="Transaction Declined", body=f" YOUR DEPOSIT OF ${deposit.amount} HAS BEEN Declined YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
            deposit.save()
            deposit.user.email_user(subject, message)
            messages.success(request, ('Transaction Declined'))
            return redirect(f'/superuser/{deposit.id}/')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/superuser/{deposit.id}/')
    return render(request, 'superuser/deposit_detail.html',{"deposit":deposit})




@manager_required
def withdraw_view(request):
    withdrawals = Transactions.objects.filter(trans_type=W).order_by('-date')
    return render(request, 'superuser/withdrawals.html',{"withdrawals":withdrawals})




@manager_required
def withdraw_detail_view(request,pk):
    withdrawal = get_object_or_404(Transactions,pk=pk)
    if request.POST:
        submit = request.POST.get('submit')
        if submit == "Approve":
            withdrawal.status = 'approved'
            withdrawal.user.withdraw_total += withdrawal.amount
            subject = "Transaction Approved"
            message = render_to_string('superuser/with-email.html', {
                'user': withdrawal.user,
                'date': timezone.now(),
                'amount': withdrawal.amount,
                'status': "Approved",
            })
            withdrawal.user.save()
            withdrawal.save()
            Notification.objects.create(user=withdrawal.user,title="Transaction Approved", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS BEEN APPROVED ")
            withdrawal.user.email_user(subject, message)
            messages.success(request, ('Transaction Approved'))
            return redirect(f'/superuser/withdrawals/{withdrawal.id}/')
        elif submit == "Decline":
            withdrawal.status = 'declined'
            subject = "Transaction Declined"
            message = render_to_string('superuser/deposite-email.html', {
                'user': withdrawal.user,
                'date': timezone.now(),
                'amount': withdrawal.amount,
                'status': "Declined",
            })
            Notification.objects.create(user=withdrawal.user,title="Transaction Declined", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS BEEN Declined YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
            withdrawal.save()
            withdrawal.user.email_user(subject, message)
            messages.success(request, ('Transaction Declined'))
            return redirect(f'/superuser/withdrawals/{withdrawal.id}/')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/superuser/withdrawals/{withdrawal.id}/')
    return render(request, 'superuser/withdrawal_detail.html',{"withdrawal":withdrawal})