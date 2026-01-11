from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import DonationRequest
from .strategy import OrganizationDonationStrategy, CitizenDonationStrategy, DonationContext
from projects.models import Project
from .forms import AdoptionForm, DonationForm
from django.db.models import Sum

@login_required
def requests_list(request):
    """عرض قائمة الطلبات للمدير"""
    if request.user.role != 'system_admin':
        messages.error(request, "ليس لديك صلاحية الوصول لهذه الصفحة")
        return redirect('home:index')
    
   
    organization_requests = DonationRequest.objects.filter(request_type='organization').order_by('-created_at')
    citizen_requests = DonationRequest.objects.filter(request_type='citizen').order_by('-created_at')
    
    context = {
        'organization_requests': organization_requests,
        'citizen_requests': citizen_requests,
        'hide_navbar': True,
    }
    return render(request, 'donations/requests_list.html', context)

@login_required
def accept_request(request, pk):
    """قبول طلب تبرع"""
    if request.user.role != 'system_admin':
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    
    
    if donation_request.request_type == 'organization':
        strategy = OrganizationDonationStrategy(donation_request)
    else:
        strategy = CitizenDonationStrategy(donation_request)
    
    context = DonationContext(strategy)
    context.process_request('accepted')
    

    if donation_request.adoption_type == 'full':
        DonationRequest.objects.filter(
            project=donation_request.project,
            request_type='organization',
            status='pending'
        ).exclude(pk=donation_request.pk).update(status='rejected')
    

    messages.success(request, 'تم قبول الطلب بنجاح')
        
    project = donation_request.project
    if project.project_type == 'community':
       
        total_funding = 0

        # جمع التمويل من التبنيات المقبولة
        accepted_adoptions = DonationRequest.objects.filter(
            project=project,
            request_type='organization',
            status='accepted'
        )
        total_funding += sum(req.amount for req in accepted_adoptions)

        
        accepted_donations = DonationRequest.objects.filter(
            project=project,
            request_type='citizen',
            status='accepted'
        )
        total_funding += sum(req.donation_amount for req in accepted_donations)

        
        if total_funding >= project.estimated_cost:
            project.status = 'completed'
            project.save()
    
    return JsonResponse({'success': True})

@login_required
def reject_request(request, pk):
    """رفض طلب تبرع"""
    if request.user.role != 'system_admin':
        return JsonResponse({'success': False, 'error': 'ليس لديك صلاحية'})
    
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    
    
    if donation_request.request_type == 'organization':
        strategy = OrganizationDonationStrategy(donation_request)
    else:
        strategy = CitizenDonationStrategy(donation_request)
    
    context = DonationContext(strategy)
    context.process_request('rejected')
    
    messages.success(request, 'تم رفض الطلب بنجاح')
    return JsonResponse({'success': True})




@login_required
def create_adoption_request(request, pk):
    """إنشاء طلب تبني مشروع (للمنظمات فقط)"""
    project = get_object_or_404(Project, pk=pk)
    
    
    if request.user.role != 'organization':
        messages.error(request, "هذه الصفحة للمنظمات فقط")
        return redirect('projects:project_detail', pk=pk)
    
    has_pending_request = DonationRequest.objects.filter(
        project=project,
        organization=request.user,
        request_type='organization',
        status='pending'
    ).exists()

    if has_pending_request:
        messages.warning(request, "لديك طلب تبني قيد المراجعة. يرجى الانتظار حتى يتم الرد عليه.")
        return redirect('projects:project_detail', pk=pk)
    has_half_donation = DonationRequest.objects.filter(
    project=project,
    request_type='citizen',
    status='accepted'
    ).aggregate(total=Sum('donation_amount'))['total'] or 0
    has_half_donation = (has_half_donation >= project.estimated_cost / 2)
    
    
    if request.method == 'POST':
        form = AdoptionForm(request.POST, project=project, user=request.user)
        if form.is_valid():
            adoption_request = form.save()
            messages.success(request, "تم إرسال طلب التبني بنجاح، في انتظار موافقة المدير")
            return redirect('projects:project_detail', pk=pk)
        else:
            messages.error(request, "يرجى تصحيح الأخطاء في النموذج")
    else:
        form = AdoptionForm(project=project, user=request.user)
    
    has_accepted_partial = DonationRequest.objects.filter(
        project=project,
        request_type='organization',
        status='accepted',
        adoption_type='partial'
    ).exists()
    

    context = {
        'form': form,
        'project': project,
        'title': 'تبني المشروع',
        'hide_navbar': True,
        'has_accepted_partial': has_accepted_partial,
        'has_half_donation': has_half_donation,
    }
    
    return render(request, 'donations/adoption_form.html', context)


def get_adoption_cost(request, pk):
    """الحصول على تكلفة التبني بناءً على النوع """
    project = get_object_or_404(Project, pk=pk)
    adoption_type = request.GET.get('type', 'full')
    
    if adoption_type == 'full':
        cost = project.estimated_cost
    else:
        cost = project.estimated_cost / 2

    
    return JsonResponse({
        'cost': float(cost),
        'formatted_cost': f'{cost:,}',
        'adoption_type': adoption_type
    })


@login_required
def create_donation_request(request, pk):
    """إنشاء طلب تبرع من مواطن"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.user.role != 'citizen':
        messages.error(request, "هذه الصفحة مخصصة للمواطنين فقط.")
        return redirect('projects:project_detail', pk=pk)

    if request.method == 'POST':
        form = DonationForm(request.POST, user=request.user, project=project)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إرسال طلب التبرع بنجاح، في انتظار موافقة المدير.")
            return redirect('projects:project_detail', pk=pk)
        else:
            messages.error(request, "يرجى تصحيح الأخطاء في النموذج.")
    else:
        form = DonationForm(user=request.user, project=project)
    
    context = {
        'form': form,
        'project': project,
        'title': 'طلب تبرع',
        'hide_navbar': True,
    }
    return render(request, 'donations/donation_form.html', context)
