from django.db import models
from django.contrib.auth.models import User

from projects.models import Project

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from functools import wraps

class Color(models.Model):
    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()
    
    @classmethod
    def create(cls, r, g, b):
        return Color(r=r, g=g, b=b)
    
    def __str_(self):
        return '[Color: (' + str(r) + ', ' + str(g) + ', ' + str(b) + ') ]'

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    color = models.ForeignKey(Color, null=True)
    
    @classmethod
    def create(cls, user):
        return cls(user=user)
        
    def __str__(self):
        return 'UserProfile: ' + self.user.username
        
def authenticate(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.user:
            return HttpResponseRedirect(reverse('accounts.views.login'))
        profile = UserProfile.objects.filter(id=request.user.id).first()
        if not profile:
            return HttpResponseRedirect(reverse('accounts.views.login'))
        return func(request, *args, **kwargs)
        
    return wrap
    