from django.shortcuts import render

from projects.models import Project, Task
from accounts.models import UserProfile, authenticate
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

@authenticate
def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
        
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project = Project.create(project_name)
        project.save()
        
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
        return HttpResponseForbidden()
    
    difficulty = request.GET.get('difficulty')
    importance = request.GET.get('importance')
    description = request.GET.get('description')

    task = Task.create(project, difficulty, importance, description)
    task.save()
    
@authenticate
def view_task(request, id):
    def render_page(task):
        params = {'task': task}
        return render(request, 'projects/view_task.html', params)
    task = Task.objects.filter(id=id).first()
    if not Task:
        return HttpResponseNotFound('<h1>Task does not exist.</h1>')
        
    # must be part of project to view task
    current_user = User.objects.filter(id=request.user.id).first()
    current_user_profile = UserProfile.objects.filter(user=current_user).first()
    if not current_user_profile in UserProfile.objects.filter(project=task.project):
        return HttpResponseForbidden()   
     
    return render_page(task)