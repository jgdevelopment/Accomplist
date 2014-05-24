from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField()
    users = models.ManyToManyField('accounts.UserProfile')

    @classmethod
    def create(cls, name):
        slug = slugify(name)
        return cls(name=name, slug=slug)
        
    def __str__(self):
        return 'Project: ' + self.name