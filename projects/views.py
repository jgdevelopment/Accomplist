from django.shortcuts import render

def create_project(request):
    def render_page():
        return render(request, 'projects/create_project.html')
    return render_page()
