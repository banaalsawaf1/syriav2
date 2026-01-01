from django.shortcuts import render
from projects.models import Project 
# Create your views here.
def index(request):
    return render(request, 'home/index.html')