from xmlrpc.client import boolean
from django.db import models
from django.contrib.auth.models import User
   
class Todo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    completed = models.BooleanField(default=False)
    class Meta:
        app_label = 'todo'
        
    def __str__(self):
        return self.name
    
    
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            app_label = 'todo'
            
    def __str__(self):
        return self.username
 