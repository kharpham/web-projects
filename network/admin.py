from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post

# Register your models here.
class UserrAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers",)

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
admin.site.register(User, UserrAdmin)
admin.site.register(Post, PostAdmin)