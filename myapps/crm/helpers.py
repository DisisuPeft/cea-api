from django.utils.timezone import localtime
from django.utils.timezone import now


def get_now():
    return localtime(now())

def get_today():
    return get_now().date()