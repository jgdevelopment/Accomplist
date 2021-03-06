from django.shortcuts import render

from projects.models import Project, Task, Link
from accounts.models import UserProfile, Color, authenticate
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound

from django.core import serializers

@authenticate
def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
        
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project = Project.create(project_name)
        project.save()
        
        print(request.user)
        current_user_profile = UserProfile.objects.get(user=request.user)
        project.users.add(current_user_profile)
        
        users = request.POST.getlist('users[]')
        for user in users:
            if User.objects.filter(username=user).exists():
                profile = UserProfile.objects.filter(user=User.objects.get(username=user)).first()
                project.users.add(profile)
                
        project.save()
        
        return HttpResponseRedirect(reverse('projects.views.view_project', args=(project.slug,)))
    
    return render_page()

def view_project(request, slug):
    def render_page(project, currentUserScore, sortedScores):
        params = {'project': project, 
                  'currentUserScore': currentUserScore,
                  'sortedScores': sortedScores}
        return render(request, 'projects/view_project.html', params)
        
    project = Project.objects.filter(slug=slug).first()
    if not project:
        return render(request, 'projects/does_not_exist.html')

    current_profile = None
    current_score = 0
    otherScores = []
    for profile in UserProfile.objects.filter(project=project):
        if profile.user == request.user:
            current_profile = profile
            current_score = project.score_for(profile)
        else:
            otherScores.append([profile, project.score_for(profile)])
            
    if not current_profile:
        return HttpResponseRedirect(reverse('accounts.views.login'))

    def sortKey(x):
        return x[1]

    return render_page(project, [current_profile, current_score], sorted(otherScores, key=sortKey))
    
def test_add_task():
    pass
    
@authenticate
def add_task(request):
    project = Project.objects.filter(slug=request.GET.get('project')).first()
    current_user = User.objects.filter(id=request.user.id).first()
    current_user_profile = UserProfile.objects.filter(user=current_user).first()

    if not current_user_profile in UserProfile.objects.filter(project=project):
        print(current_user_profile)
        return HttpResponseForbidden()
    
    difficulty = request.GET.get('difficulty')
    importance = request.GET.get('importance')
    description = request.GET.get('description')

    task = Task.create(project, difficulty, importance, description)
    task.save()
    
@authenticate
def view_task(request, id):
    def render_page(task, links):
        completer = ''
        if task.completed_by != None:
            completer = task.completed_by.user.username
        params = {'task': task, 'links': links, 'iterate_importance': ['0'] * task.importance, 'iterate_difficulty': ['0'] * task.difficulty, 'completed':(task.completed_by != None),
        'completer':completer}
        return render(request, 'projects/view_task.html', params)
    task = Task.objects.filter(id=id).first()
    if not Task:
        return HttpResponseNotFound('<h1>Task does not exist.</h1>')
        
    # must be part of project to view task
    current_user = User.objects.filter(id=request.user.id).first()
    current_user_profile = UserProfile.objects.filter(user=current_user).first()
    if not current_user_profile in UserProfile.objects.filter(project=task.project):
        return HttpResponseForbidden()   
    
    links = list(Link.objects.filter(task=task))
     
    return render_page(task, links)
    
@authenticate
def complete_task(request):
    task = Task.objects.filter(id=request.GET.get('task')).first()
    if not task:
        return HttpResponseNotFound('<h1>Task does not exist.</h1>')
        
    project = task.project
        
    # must be part of project to view task
    current_user = User.objects.filter(id=request.user.id).first()
    current_user_profile = UserProfile.objects.filter(user=current_user).first()
    if not current_user_profile in UserProfile.objects.filter(project=task.project):
        return HttpResponseForbidden()
        
    if task.completed_by:
        return HttpResponse('Task already completed.')
    task.completed_by = current_user_profile
    task.save()
    return HttpResponse('Task completed.')
    
@authenticate
def get_tasks(request):
    project = Project.objects.filter(slug=request.GET.get('project')).first()
    if not project:
        return HttpResponseNotFound('<h1>Project does not exist.</h1>')
        
    tasks = list(Task.objects.filter(project=project))
    def sortKey(x):
        return -(x.importance + x.difficulty)
    tasks = sorted(tasks, key=sortKey)
    
    return HttpResponse(serializers.serialize("json", tasks), content_type='application/json')

def add_link(request):
    task = Task.objects.filter(id=request.GET.get('task')).first()
    if not task:
        return HttpResponseNotFound('<h1>Task does not exist.</h1>')
    name = request.GET.get('name')
    url = request.GET.get('url')
        
    link = Link.create(task, name, url)
    link.save()
    
    return HttpResponse('<h1>Added link.</h1>')