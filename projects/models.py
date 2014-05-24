from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField()

    @classmethod
    def create(cls, name):
        slug = slugify(name)
        return cls(name=name, slug=slug)
        
    def __unicode__(self):
        return 'Project: ' + self.name