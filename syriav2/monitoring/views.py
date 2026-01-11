from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProjectStageUpdateForm
from .models import ProjectStageUpdate
from .state import StageStateFactory
from projects.models import Project

@login_required
def project_stage_update_view(request):
    if request.user.role != 'contractor':
        messages.error(request, "هذه الصفحة متاحة فقط للمتعهدين.")
        return redirect('home:index')

    if request.method == 'POST':
        form = ProjectStageUpdateForm(request.POST, request.FILES, contractor=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.full_clean()

            
            last_update = ProjectStageUpdate.objects.filter(project=update.project).order_by('-stage_number').first()
            expected_stage = (last_update.stage_number + 1) if last_update else 1
            if update.stage_number != expected_stage:
                messages.error(request, f"يجب أن تُحدّث المرحلة {expected_stage} الآن.")
                return render(request, 'monitoring/project_stages_update.html', {'form': form})

            update.save()

           
            state = StageStateFactory.get_state(update.stage_number)
            state.handle(update)

            messages.success(request, f'تم تحديث حالة المشروع إلى المرحلة "{update.stage_name}" بنجاح.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = ProjectStageUpdateForm(contractor=request.user)
    context = {
        'hide_navbar' : True ,
        'form': form ,
    }
    return render(request, 'monitoring/project_stages_update.html', context)


def project_stages_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    
    can_view_reports = False
    if request.user.is_authenticated:
     can_view_reports = (
        request.user.role == 'system_admin' or
        (request.user.role == 'contractor' and project.contractor == request.user) or
        request.user.role == 'organization' 
    )

    stages = project.stage_updates.all().order_by('stage_number')


    total_completion = sum(stage.completion_percentage for stage in stages)
    

    
    remaining_completion = 100 - total_completion

    
    latest_stage = stages.last()
    remaining_cost = latest_stage.remaining_cost if latest_stage else project.estimated_cost
    spent_cost = project.estimated_cost - remaining_cost

    
    remaining_duration = latest_stage.remaining_duration if latest_stage else project.duration

    context = {
        'project': project,
        'stages': stages,
        'can_view_reports': can_view_reports,
        'total_completion': min(total_completion, 100),  
        'remaining_completion': remaining_completion,
        'spent_cost': spent_cost,
        'remaining_cost': remaining_cost,
        'remaining_duration': remaining_duration,
        'hide_navbar' : True ,
    }
    return render(request, 'monitoring/project_stages_detail.html', context)

@login_required
def admin_updates_management_view(request):
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول إلى هذه الصفحة.")
        return redirect('home:index')

    projects = Project.objects.filter(
        is_cancelled=False
    ).select_related('contractor').order_by('-updated_at')

    context = {
        'projects': projects,
        'hide_navbar': True,
    }
    return render(request, 'monitoring/admin_updates_management.html', context)
