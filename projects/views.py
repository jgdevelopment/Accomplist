from django.shortcuts import render

from projects.models import Project
from accounts.models import UserProfile
from django.contrib.auth.models import User

def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
        
    print(request.user)
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
        
    return render_page()