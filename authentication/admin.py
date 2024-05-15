from django.contrib import admin

# # Register your models here.
from .models import UserImage

# # Register your models here.
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'user')

admin.site.register(UserImage, UserImageAdmin)