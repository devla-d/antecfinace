from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import random
import string
import json
from uuid import uuid4

from account.models import Account



class Notification(models.Model):
    user =  models.ForeignKey(Account,related_name='user_notify', on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True,null=True) 
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

 


    def __str__(self):
        return f"{self.user.username} "




class Packages(models.Model):


    hours= models.IntegerField()   
    name = models.CharField(max_length=40)
    percent = models.IntegerField()
    min_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=0)
    ref_percent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"








class Transactions(models.Model):
    user =  models.ForeignKey(Account,related_name='user_transactions', on_delete=models.CASCADE,null=True, blank=True)
    wallet_address = models.CharField(max_length=50,blank=True,null=True) 
    amount = models.IntegerField( blank=True,null=True)
    coin_tpye = models.CharField(max_length=50,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True) 
    approved_date = models.DateTimeField(blank=True,null=True) 
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=40,default="pending") 
    trans_type = models.CharField(max_length=50)



    def __str__(self):
        return f"{self.user.username} :  {self.trans_type}"




STATUS = (
    ("active","active"),
    ("inactive","inactive"),
    ("pending","pending"),
    ("completed","completed"),
)

class Investments(models.Model):

    user =  models.OneToOneField(Account, on_delete = models.CASCADE)
    amount_invested = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False) 
    end_date =  models.DateTimeField(blank=True,null=True)
    start_date =  models.DateTimeField(blank=True,null=True)
    crediting_date =  models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=40, choices=STATUS,default="inactive")
    amount_earn = models.IntegerField(default=0)
    package = models.ForeignKey(Packages,on_delete = models.CASCADE, related_name="pack" , blank=True, null=True)
 
    def __str__(self):
        return f"{self.user.username} :  {self.amount_invested}"




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_investmet(sender,instance=None, created=False, **kwargs):
    if created:
        Investments.objects.create(user=instance,amount_invested=0)