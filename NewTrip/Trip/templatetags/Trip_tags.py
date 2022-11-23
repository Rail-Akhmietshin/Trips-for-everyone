from django import template

from Trip.models import Trip
from datetime import datetime

register = template.Library()
#
@register.simple_tag
def get_date():
    return datetime.now().strftime("%Y-%m-%d")


@register.simple_tag
def username_post_created(pk):
    return Trip.objects.get(pk=pk).trip_user.username

@register.simple_tag
def number_phone_post_created(pk):
    return Trip.objects.get(pk=pk).trip_user.number_phone

