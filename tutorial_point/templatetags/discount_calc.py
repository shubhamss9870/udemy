
from django import template
from ..models import *
register = template.Library()

@register.simple_tag
def price_discount(price,discount):
    if discount is None or discount==0:
        return price
    else :
        return int(price * ((100-discount)*0.01))

@register.simple_tag
def is_enroll(request, course):
    user = None
    try:
        if not request.session['name']:
            return False
    except:
        return False
    user = datas.objects.get(name = request.session['name'])
    try:
        user = usercourse.objects.get(username = user, course_name = course)

        return True
    except:
        return False