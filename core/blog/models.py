from django.db import models
from accounts.models import Profile


class Post(models.Model):
    author=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)                  
    title=models.CharField(max_length=255)
    image=models.ImageField(blank=True,null=True)
    status=models.BooleanField()
    category=models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    published_date=models.DateTimeField()

    def __str__(self):
        return self.title

class Category(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

