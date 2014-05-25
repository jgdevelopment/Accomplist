from django.db import models
from django.contrib.auth.models import User

from projects.models import Project

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from functools import wraps

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
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
    