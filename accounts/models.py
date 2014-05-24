from django.db import models
from django.contrib.auth.models import User

from projects.models import Project

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    projects = models.ManyToManyField(Project)
    
    @classmethod
    def create(cls, user):
        return cls(user=user)
        
    def __str__(self):
        return 'UserProfile: ' + self.user.username