from django.contrib import admin
from .models import RegisterUser, Blog, Comment

# Register your models here.
admin.site.register(RegisterUser)
admin.site.register(Blog)
admin.site.register(Comment)