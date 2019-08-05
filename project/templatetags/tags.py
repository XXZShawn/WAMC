from django import template
from django.utils.safestring import mark_safe
from FBA import settings
import hashlib

register = template.Library()
@register.filter
def filter_t(x,y):
    return str(x)+str(y)

# def filter_v(x):
#     md5 = hashlib.md5()
#     md5.update(bytes(x,encoding="utf-8"))
#     x = md5.hexdigest()
#     return "/view/media/image/%s.png"%x
    
@register.filter
def multiply(x,y):
    return (x-1)*y