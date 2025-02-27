# blog/models.py
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("can_view", "Can view posts"),
            ("can_create", "Can create posts"),
            ("can_edit", "Can edit posts"),
            ("can_delete", "Can delete posts"),
        ]
        
    def __str__(self):
        return self.title