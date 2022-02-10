from django.utils import timezone
from datetime import timedelta
from .models import Transactions,Notification,Investments,Packages





def get_deadline(h):
	return timezone.now() + timedelta(hours=h)

def earnings(amount , perc): 
    p = (perc/100) * amount
    return p + amount