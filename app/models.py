from django.db import models

# Create your models here.
class RegisterUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Blog(models.Model):
    title = models.CharField(max_length=50, primary_key=True, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}-{self.created_at}'