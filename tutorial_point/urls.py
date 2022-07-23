from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('', views.show, name='index'),
    path('contact/', views.contact, name="con"),
    path('about/', views.about, name="ab"),
    path('signup/', views.signup, name='sign'),
    path('log_in/', views.login, name="login"),
    path('logout/', views.logout, name = 'logout'),
    path('course/<str:slug>', views.course_information, name = 'course'),
    path('checkout/<str:slug>', views.checkout, name="checkout"),
    path('verify_payment', views.verify_payment, name="verifypayment")
]
