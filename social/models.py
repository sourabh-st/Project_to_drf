
from django.db import models
from django.contrib.auth import get_user_model

django_user = get_user_model()

class MyProfile(models.Model):
    user = models.OneToOneField(django_user,on_delete=models.CASCADE)
    profilename = models.CharField(max_length=40,null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    address = models.TextField(max_length=100,null=True,blank=True)
    stat = models.CharField(max_length=40,null=True,blank=True)
    gender = models.CharField(max_length=40,null=True,blank=True)
    description = models.TextField(max_length=100,null=True,blank=True)
    profilepic = models.ImageField(upload_to = "images", null=True,blank=True)
    followers = models.ManyToManyField(django_user, blank=True, related_name='follower')

    def __str__(self):
        return str(self.profilename)

class MyPost(models.Model):
    pic = models.ImageField(upload_to = "images", null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(django_user,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.subject)
