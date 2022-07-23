from django.db import models

# Create your models here.
class datas(models.Model):
    name = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    mobile = models.IntegerField()

    def __str__(self):
        return self.name

class course_dtls(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image/')
    def __str__(self):
        return self.title

class video(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    s_no = models.IntegerField()
    course_name = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class usercourse(models.Model):
    username = models.ForeignKey(datas, on_delete=models.CASCADE)
    course_name = models.ForeignKey(course_dtls, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.name




class payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    user = models.ForeignKey(datas, on_delete=models.CASCADE)
    course = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    user_course = models.ForeignKey(usercourse, null = True, on_delete=models.CASCADE,)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.order_id

class Refcode(models.Model):
    code = models.CharField(max_length=100)
    user_course = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.code

class course_info(models.Model):
    desc = models.CharField(max_length=500)
    course = models.ForeignKey(course_dtls, on_delete= models.CASCADE)

    class Meta:
        abstract = True

class learning (course_info):
    pass

class pre_req(course_info):
    pass
