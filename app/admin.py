from django.contrib import admin
from .models import RegisterUser, Blog

# Register your models here.
admin.site.register(RegisterUser)
admin.site.register(Blog)