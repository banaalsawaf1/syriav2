from django.shortcuts import render
from projects.models import Project 

def index(request):
   
    priority_projects = Project.objects.filter(
        priority_score__gt=0
    ).order_by('-priority_score')[:3]

    
    
    ordered_projects = []
    labels = ["أهم مشروع", "متوسط الأهمية", "أقل أهمية"]
    icons = ["fas fa-crown text-warning", "fas fa-medal text-secondary", "fas fa-award text-info"]
    
    for i, proj in enumerate(priority_projects):
        ordered_projects.append({
            'project': proj,
            'level': labels[i],
            'icon': icons[i],
            'rank': i + 1
        })

    
    in_progress_projects = Project.objects.filter(
         status__in=['in_progress', 'completed'],
        is_cancelled=False
    )
    context = {
        'priority_projects': ordered_projects,
        'in_progress_projects': in_progress_projects, 
    }
    return render(request, 'home/index.html', context)
