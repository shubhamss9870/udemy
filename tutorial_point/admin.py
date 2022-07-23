from django.contrib import admin
from .models import *
# Register your models here.

class all_learning(admin.TabularInline):
    model = learning


class all_pre_req(admin.TabularInline):
    model = pre_req



class all_video_info(admin.ModelAdmin):
    inlines = [all_learning, all_pre_req]



admin.site.register(datas)
admin.site.register(course_dtls, all_video_info)
admin.site.register(video)
admin.site.register(usercourse)
admin.site.register(payment)
admin.site.register(Refcode)

