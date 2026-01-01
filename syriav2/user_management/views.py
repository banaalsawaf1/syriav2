from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from accounts.models import User
from projects.models import Project
from .forms import UserCreateForm, UserEditForm

@login_required
def user_list(request):
    """عرض قائمة المستخدمين للمدير فقط"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    
    users = User.objects.exclude(role='system_admin').order_by('-date_joined')
    
    
    users_count = users.count()
    deleted_users_count = users.filter(is_deleted=True).count()
    
    
    citizen_count = users.filter(role='citizen').count()
    organization_count = users.filter(role='organization').count()
    contractor_count = users.filter(role='contractor').count()
    
    context = {
        'users': users,
        'users_count': users_count,
        'deleted_users_count': deleted_users_count,
        'citizen_count': citizen_count,
        'organization_count': organization_count,
        'contractor_count': contractor_count,
        'hide_navbar': True
    }
    return render(request, 'user_management/user_list.html', context)

@login_required
def users_by_role(request, role):
    """عرض المستخدمين حسب الدور"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    
    valid_roles = ['citizen', 'organization', 'contractor']
    if role not in valid_roles:
        messages.error(request, "الدور غير صالح")
        return redirect('user_management:user_list')
    
    
    role_names = {
        'citizen': 'مواطن',
        'organization': 'منظمة',
        'contractor': 'متعهد',
    }
    
    
    users = User.objects.filter(role=role).order_by('-date_joined')
    
    
    for user in users:
        if role == 'contractor':
            user.assigned_projects = Project.objects.filter(contractor=user, is_cancelled=False)
        elif role == 'organization':
            
            user.adopted_projects = []  
    
    context = {
        'users': users,
        'role': role,
        'role_name': role_names[role],
        'hide_navbar': True
    }
    return render(request, 'user_management/users_by_role.html', context)

@login_required
def user_create(request):
    """إنشاء مستخدم جديد"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'تم إنشاء المستخدم {user.username} بنجاح')
            return redirect('user_management:user_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = UserCreateForm()
    
    context = {
        'form': form,
        'title': 'إضافة مستخدم جديد',
        'hide_navbar': True
    }
    return render(request, 'user_management/user_form.html', context)

@login_required
def user_update(request, pk):
    """تعديل مستخدم موجود"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    user = get_object_or_404(User, pk=pk)
    
    
    if user.role == 'system_admin':
        messages.error(request, "لا يمكن تعديل مدير النظام")
        return redirect('user_management:user_list')
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث المستخدم {user.username} بنجاح')
            return redirect('user_management:user_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'title': 'تعديل المستخدم',
        'hide_navbar': True
    }
    return render(request, 'user_management/user_form.html', context)

@login_required
def user_delete(request, pk):
    """حذف مستخدم (حذف منطقي)"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
    user = get_object_or_404(User, pk=pk)
    
    
    if user.role == 'system_admin':
        messages.error(request, "لا يمكن حذف مدير النظام")
        return redirect('user_management:user_list')
    
    
    if user.role == 'contractor' and Project.objects.filter(contractor=user, is_cancelled=False).exists():
        messages.error(request, "لا يمكن حذف متعهد معين في مشاريع قيد التنفيذ")
        return redirect('user_management:user_list')
    
    if request.method == 'POST':
        user.is_deleted = True
        user.save()
        messages.success(request, f'تم حذف المستخدم {user.username} بنجاح')
        return redirect('user_management:user_list')
    
    context = {
        'user': user,
        'hide_navbar': True
    }
    return render(request, 'user_management/user_confirm_delete.html', context)