from django.shortcuts import render

from projects.models import Project
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
        
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        project = Project.create(project_name)
        project.save()
        
        if not UserProfile.objects.filter(user=request.user).exists():
            profile = UserProfile.create(user=request.user)
            profile.save()
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
    def render_page(project):
        params = {'project': project}
        return render(request, 'projects/view_project.html', params)
        
    project = Project.objects.filter(slug=slug).first()
    if not project:
        return render(request, 'projects/does_not_exist.html')
    print(project.users.all())
    return render_page(project)