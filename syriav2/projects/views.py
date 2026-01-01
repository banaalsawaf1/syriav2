from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Project
from .forms import ProjectForm, ProjectEditForm, AssignContractorForm
from accounts.models import User
from .factories import ProjectFactory
import folium
import json
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import User

@login_required
def project_list(request):
    """عرض قائمة المشاريع للمدير فقط"""
    if request.user.role != 'system_admin':
        messages.error(request, 'ليس لديك صلاحية الوصول لهذه الصفحة')
        return redirect('home:index')
    
    
    projects = Project.objects.all().order_by('-created_at')
    
    
    projects_count = projects.count()
    pending_count = projects.filter(status='pending', is_cancelled=False).count()
    in_progress_count = projects.filter(status='in_progress', is_cancelled=False).count()
    completed_count = projects.filter(status='completed', is_cancelled=False).count()
    cancelled_count = projects.filter(Q(status='cancelled') | Q(is_cancelled=True)).count()
    
    
    comprehensive_count = projects.filter(project_type='comprehensive').count()
    community_count = projects.filter(project_type='community').count()
    development_count = projects.filter(project_type='development').count()


    context = {
        'projects': projects,
        'projects_count': projects_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'comprehensive_count': comprehensive_count,
        'community_count': community_count,
        'development_count': development_count,
        'hide_navbar': True
    }
    
    return render(request, 'projects/project_list.html', context)


@login_required
def project_create(request):
    """إنشاء مشروع جديد"""
    if request.user.role != 'system_admin':
        messages.error(request, 'ليس لديك صلاحية الوصول لهذه الصفحة')
        return redirect('home:index')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                project_type = form.cleaned_data['project_type']
                
                
                factory = ProjectFactory.get_factory(project_type)
                project = factory.create_project(
                    form.cleaned_data,
                    request.user
                )
                project.created_by = request.user
                project.save()
                messages.success(request, 'تم إضافة المشروع بنجاح')
                return redirect('projects:project_list')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء حفظ المشروع: {str(e)}')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'title': 'إضافة مشروع جديد',
        'hide_navbar': True
    }
    
    return render(request, 'projects/project_form.html', context)


@login_required
def project_update(request, pk):
    """تعديل مشروع موجود"""
    if request.user.role != 'system_admin':
        messages.error(request, 'ليس لديك صلاحية الوصول لهذه الصفحة')
        return redirect('home:index')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectEditForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المشروع بنجاح')
            return redirect('projects:project_list')
    else:
        form = ProjectEditForm(instance=project)
    
    context = {
        'form': form,
        'title': 'تعديل المشروع',
        'project': project,
        'hide_navbar': True
    }
    
    return render(request, 'projects/project_form.html', context)


@login_required
def project_delete(request, pk):
    """حذف مشروع"""
    if request.user.role != 'system_admin':
        messages.error(request, 'ليس لديك صلاحية الوصول لهذه الصفحة')
        return redirect('home:index')
    
    project = get_object_or_404(Project, pk=pk)
    
    if project.status == 'in_progress':
        messages.error(request, " لا يمكن حذف مشروع قيد التنفيذ")
        return redirect('projects:project_list')
    
    if request.method == 'POST':
        project.is_cancelled = True
        project.status = 'cancelled'
        project.save()
        messages.success(request, 'تم حذف المشروع بنجاح')
        return redirect('projects:project_list')
    
    context = {
        'project': project,
    }
    
    return render(request, 'projects/project_confirm_delete.html', context)


def project_detail(request, pk):
    """عرض تفاصيل المشروع للجميع (زائر، مواطن، منظمة، مدير)"""
    project = get_object_or_404(Project, pk=pk)
    
    
    if not request.user.is_authenticated:  
        if project.is_cancelled:
            messages.error(request, "لا يمكن عرض المشروع الملغى")
            return redirect('home:index')
    elif request.user.role != 'system_admin':  
        if project.is_cancelled:
            messages.error(request, "لا يمكن عرض المشروع الملغى")
            return redirect('home:index')
    
    
    map_html = None
    if project.latitude and project.longitude:
        
        map_center = [float(project.latitude), float(project.longitude)]
        
        
        if project.project_type == 'development':
            marker_color = '#2b6b42'
        elif project.damage_type == 'total':
            marker_color = '#dc3545'  
        elif project.damage_type == 'partial':
            marker_color = '#fd7e14'  
        else:
            marker_color = '#2b6b42'  
        
        
        m = folium.Map(location=map_center, zoom_start=15)
        
       
        folium.Marker(
            location=map_center,
            popup=f"مشروع: {project.name}",
            tooltip="موقع المشروع",
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)
        
        
        map_html = m._repr_html_()
    
    
    formatted_cost = f"{project.estimated_cost:,}" if project.estimated_cost else "0"
    
    
    chart_data_json = json.dumps({
        'cost': float(project.estimated_cost or 0),
        'area': float(project.area or 0),
        'duration': project.duration or "غير محدد"
    }, cls=DjangoJSONEncoder)
    
    if request.user.is_authenticated:
        user_role = request.user.role
        is_authenticated = True
    else:
        user_role = 'visitor'
        is_authenticated = False

    context = {
        'project': project,
        'map_html': map_html,
        'formatted_cost': formatted_cost,
        'chart_data_json': chart_data_json,  
        'hide_navbar': True,
        'user_role': user_role,
        'is_authenticated': is_authenticated,
    }
    
    return render(request, 'projects/project_detail.html', context)


@login_required
def project_change_status(request, pk):
    """تغيير حالة المشروع"""
    if request.user.role != 'system_admin':
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    
    project = get_object_or_404(Project, pk=pk)
    status = request.GET.get('status')
    
    if status in ['pending', 'in_progress', 'completed', 'cancelled']:
        project.status = status
        project.save()
        return JsonResponse({'success': True, 'new_status': project.get_status_display()})
    
    return JsonResponse({'success': False, 'error': 'حالة غير صالحة'})

@login_required
def projects_by_type(request, project_type):
    """عرض المشاريع حسب النوع"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    
    valid_types = ['comprehensive', 'community', 'development']
    if project_type not in valid_types:
        messages.error(request, "نوع المشروع غير صالح")
        return redirect('projects:project_list')
    
    
    type_names = {
        'comprehensive': 'إعادة الإعمار الشاملة',
        'community': 'الدعم المجتمعي',
        'development': 'التنمية الإنشائية الجديدة'
    }
    
    
    projects = Project.objects.filter(project_type=project_type)
    
    
    projects_count = projects.count()
    
    context = {
        'projects': projects,
        'projects_count': projects_count,
        'project_type': project_type,
        'project_type_name': type_names[project_type],
        'hide_navbar': True
    }
    
    return render(request, 'projects/projects_by_type.html', context)
def projects_by_type_public(request, project_type):
    """عرض المشاريع حسب النوع للزوار والمواطنين والمنظمات (3 صور في كل صف)"""
    
    valid_types = ['comprehensive', 'community', 'development']
    if project_type not in valid_types:
        messages.error(request, "نوع المشروع غير صالح")
        return redirect('home:index')
    
    
    type_names = {
        'comprehensive': 'إعادة الإعمار الشاملة',
        'community': 'الدعم المجتمعي',
        'development': 'التنمية الإنشائية الجديدة'
    }
    
    
    projects = Project.objects.filter(
        project_type=project_type,
        is_cancelled=False
    ).order_by('-created_at')
    
    projects_count = projects.count()
    
    context = {
        'projects': projects,
        'projects_count': projects_count,
        'project_type': project_type,
        'project_type_name': type_names[project_type],
        'hide_navbar': True
    }
    
    return render(request, 'projects/projects_by_type_public.html', context)


@login_required
def assign_contractor(request, pk):
    """تعيين متعهد للمشروع"""
    if request.user.role != 'system_admin':
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = AssignContractorForm(request.POST)
        if form.is_valid():
            try:
                contractor = form.save(project)
                messages.success(request, f'تم تعيين المتعهد {contractor.username} بنجاح للمشروع')
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'بيانات غير صالحة'})
    
    
    form = AssignContractorForm()
    return render(request, 'projects/assign_contractor_modal.html', {'form': form, 'project': project})

@login_required
def get_contractors(request):
    """الحصول على قائمة المتعهدين (لـ AJAX)"""
    if request.user.role != 'system_admin':
        return JsonResponse({'contractors': []})
    
    from accounts.models import User
    contractors = User.objects.filter(role='contractor', is_deleted=False).values('id', 'username')
    return JsonResponse({'contractors': list(contractors)})