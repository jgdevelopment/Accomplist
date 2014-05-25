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
        
    def score_for(self, user):
        score = 0
        for task in Task.objects.filter(completed_by=user):
            score += (task.difficulty + task.importance)
        return score
        
    def __str__(self):
        return 'Project: ' + self.name
        
class Task(models.Model):
    project = models.ForeignKey('projects.Project')
    difficulty = models.IntegerField()
    importance = models.IntegerField()
    description = models.CharField(max_length=1000)
    completed_by = models.ForeignKey('accounts.UserProfile', null=True, blank=True)
    
    @classmethod
    def create(cls, project, difficulty, importance, description):
        return Task(project=project, difficulty=difficulty, importance=importance, description=description, completed_by=None)