from django.shortcuts import render
# Create your views here.

def home(request):
    def render_page():
        params = {}
        return render(request, 'main/home.html', params)
        
    return render_page()
