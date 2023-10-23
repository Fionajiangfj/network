from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('username', 'likes')
    
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','followers')


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)