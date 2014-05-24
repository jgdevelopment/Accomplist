from django.shortcuts import render

from projects.models import Project
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
        
    if not UserProfile.objects.filter(user=request.user).exists():
        prof = UserProfile.create(request.user)
        prof.save()
    current_user_profile = UserProfile.objects.get(user=request.user)
        
    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        users = request.POST.getlist('users[]')
        project = Project.create(project_name)
        project.save()
        current_user_profile.projects.add(project)
        project.users.add(current_user_profile)
        for user in users:
            if User.objects.filter(username=user).exists():
                u = User.objects.get(username=user)
                profile = UserProfile.objects.get(user=u)
                project.users.add(profile)
        project.save()
        return HttpResponseRedirect(reverse('projects.views.view_project', args=(project.slug,)))
    
    return render_page()
    
def view_project(request, slug):
    def render_page(project):
        params = {'project': project}
        return render(request, 'projects/view_project.html', params)
        
    print(slug)
    project = Project.objects.filter(slug=slug).first()
    if not project:
        return render(request, 'projects/does_not_exist.html')
    return render_page(project)