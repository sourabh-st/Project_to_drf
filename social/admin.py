from django.contrib import admin
from social.models import MyProfile, MyPost
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(User)
@admin.register(User)
class MyUserProfile(admin.ModelAdmin):
    list_display = ['id','username','email']
# Register your models here.
@admin.register(MyProfile)
class MyProfileAdmin(admin.ModelAdmin):
    list_display = ['id','profilename','age']


@admin.register(MyPost)
class MyPostAdmin(admin.ModelAdmin):
    list_display = ['id','subject','pic']
