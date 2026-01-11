from django.db import models
from accounts.models import User
from projects.models import Project

class DonationRequest(models.Model):
    """نموذج أساسي للطلب، يستخدم Strategy Pattern"""
    REQUEST_TYPES = [
        ('organization', 'منظمة'),
        ('citizen', 'مواطن'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]
    
    ADOPTION_TYPES = [
        ('full', 'كامل'),
        ('partial', 'جزئي'),
    ]
    

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, verbose_name='نوع الطلب')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='حالة الطلب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
   
    organization = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                                     limit_choices_to={'role': 'organization'}, 
                                     verbose_name='المنظمة', related_name='organization_requests')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='المشروع')
    adoption_type = models.CharField(max_length=20, choices=ADOPTION_TYPES, null=True, blank=True, 
                                     verbose_name='نوع التبني')
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, 
                                 verbose_name='المبلغ المطلوب')
    message = models.TextField(blank=True, verbose_name='رسالة الطلب')
    
   
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                limit_choices_to={'role': 'citizen'},
                                verbose_name='المواطن', related_name='citizen_requests')
    donation_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                          verbose_name='مبلغ التبرع')
    
    
    
    confirmation = models.BooleanField(default=False, verbose_name='تأكيد المنظمة')
    
    class Meta:
        verbose_name = 'طلب تبرع'
        verbose_name_plural = 'طلبات التبرع'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.request_type == 'organization':
            return f'طلب تبني من {self.organization.username} للمشروع {self.project.name}'
        else:
            return f'طلب تبرع من {self.citizen.username} للمشروع {self.project.name}'
