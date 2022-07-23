from django.shortcuts import redirect,render
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password
import razorpay
from time import time
from django.views.decorators.csrf import csrf_exempt

from udemy.settings import *
client = razorpay.Client(auth=(key_id, secret_id))


# Create your views here.
def show(request):
    course_info = course_dtls.objects.all()
    return render(request, 'index.html', {'course_list':course_info})
def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')
def signup(request):
    if request.method =="POST":
        name = request.POST.get('name')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        c = datas(name = name, lname = lname, email = email, password = make_password(password), mobile = mobile)
        c.save()
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            fetch_info = datas.objects.get(email = email)
            if(check_password(password, fetch_info.password)):
                print('you have entered correct password')
                request.session['name']= fetch_info.name
                request.session['email'] = fetch_info.email
                return redirect('index')
            else:
                return HttpResponse('please enter a valid password')
        except:
            return HttpResponse("please enter a valid email")

def logout(request):
    request.session.clear()
    return redirect("index")

def course_information(request,slug):

    fetch_dtls = course_dtls.objects.get(slug = slug)
    s_no = request.GET.get('serial_no')
    videos = None
    if s_no is None:
        s_no = 1
    try:
        videos = video.objects.get(course_name = fetch_dtls, s_no = s_no)
        if videos.is_preview is False:
            if request.session.get('name') is None:
                return redirect('index')
            else:
                user_id = datas.objects.get(email = request.session['email'])
                try:
                    user_course = usercourse.objects.get(username = user_id, course_name = fetch_dtls)
                except:
                    return redirect('checkout', slug = fetch_dtls.slug)
    except:
      return redirect('index')

    return render(request, 'course_dtls.html',{'co_dtls':fetch_dtls, 'video':videos})

def checkout(request, slug):
    course = course_dtls.objects.get(slug = slug)
    user_id = datas.objects.get(email= request.session['email'])
    action= request.GET.get('action')
    coup = request.GET.get('coupon')
    error = None
    cpn_code_msg = None
    amount = None
    order_ids = None
    notes = None
    cpn_code = None



    if error is None:
        amount = int(course.price * (100 - course.discount) * 0.01*100)

    if coup :
        try:
            cpn_code = Refcode.objects.get(code = coup)
            amount = int(course.price * (100 - cpn_code.discount) * 0.01*100)
        except:
            cpn_code_msg = "Invalid coupon code"

    if action == "create_payment":
        currency= "INR"
        receipt = F'Udemy{int(time())}'

        notes = {
            'user': user_id.name,
            'email': user_id.email
            }
        data = {
                "amount":amount,
                "currency":currency,
                "receipt" :receipt,
                "notes" : notes
        }

        orders = client.order.create(data=data)
        order_ids = orders.get('id')
        payments = payment()
        payments.order_id = order_ids
        payments.user = user_id
        payments.course = course
        payments.save()
        if coup == "":
            cpn_code_msg = "Please enter a code"


    context = {
            'user_id': user_id,
            'course':course,
            'order_id': order_ids,
            'amount' : amount,
            'notes' : notes,
            'cpn_code_msg' : cpn_code_msg,
            'coup' : cpn_code
            }

    return render(request, 'checkout.html',context = context)


@csrf_exempt
def verify_payment(request):
    data = request.POST

    payment_id = data['razorpay_payment_id']
    razor_order_id = data['razorpay_order_id']
    payments = payment.objects.get(order_id = razor_order_id)
    payments.payment_id = payment_id
    payments.status = True
    user_courses = usercourse(username=payments.user, course_name = payments.course)
    user_courses.save()
    payments.user_course = user_courses
    payments.save()

    try:
        return redirect("index")
    except:
        return HttpResponse('Successfully')