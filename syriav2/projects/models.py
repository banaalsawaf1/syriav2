from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import os

User = get_user_model()

class Project(models.Model):
    """نموذج المشروع الرئيسي"""
    
    
    PROJECT_TYPES = [
        ('comprehensive', 'إعادة الإعمار الشاملة'),
        ('community', 'الدعم المجتمعي'),
        ('development', 'التنمية الإنشائية الجديدة'),
    ]
    
    
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    ]
    
    
    DAMAGE_TYPES = [
        ('total', 'كلي'),
        ('partial', 'جزئي'),
    ]
    
    
    GOVERNORATES = [
        ('damascus', 'دمشق'),
        ('aleppo', 'حلب'),
        ('homs', 'حمص'),
        ('hama', 'حماة'),
        ('latakia', 'اللاذقية'),
        ('tartus', 'طرطوس'),
        ('daraa', 'درعا'),
        ('as_suwayda', 'السويداء'),
        ('raqqa', 'الرقة'),
        ('deir_ez_zor', 'دير الزور'),
        ('hasakah', 'الحسكة'),
        ('idlib', 'إدلب'),
        ('rural_damascus', 'ريف دمشق'),
    ]
    
    
    name = models.CharField(max_length=200, verbose_name='اسم المشروع')
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES, verbose_name='نوع المشروع')
    description = models.TextField(verbose_name='وصف تفصيلي عن المشروع')
    damage_type = models.CharField(max_length=50, choices=DAMAGE_TYPES, verbose_name='نوع الضرر', blank=True, null=True)
    address = models.TextField(verbose_name='العنوان')
    governorate = models.CharField(max_length=50, choices=GOVERNORATES, verbose_name='المحافظة')
    
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='خط العرض')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='خط الطول')
    
   
    image1 = models.ImageField(upload_to='project_images/', verbose_name='الصورة الأولى')
    image2 = models.ImageField(upload_to='project_images/', verbose_name='الصورة الثانية')
    image3 = models.ImageField(upload_to='project_images/', verbose_name='الصورة الثالثة')
    image4 = models.ImageField(upload_to='project_images/', verbose_name='الصورة الرابعة')
    
    
    estimated_cost = models.IntegerField( verbose_name='التكلفة المقدرة' , help_text='بالدولار الأمريكي (USD)')
    duration = models.CharField(max_length=100, blank=True, verbose_name='المدة المقدرة (بالأيام)')
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='المساحة (م²)')
    priority_score = models.IntegerField(default=0, verbose_name='درجة الأولوية')
    
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='حالة المشروع')
    is_cancelled = models.BooleanField(default=False, verbose_name='ملغى نهائياً')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects', verbose_name='تم الإنشاء بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
   
    contractor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='contracted_projects',verbose_name='المتعهد المعين')
    
    class Meta:
        verbose_name = 'مشروع'
        verbose_name_plural = 'المشاريع'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_project_images(self):
        """الحصول على جميع صور المشروع"""
        images = []
        for i in range(1, 5):
            image_field = getattr(self, f'image{i}')
            if image_field:
                images.append(image_field.url)
        return images
    
    def save(self, *args, **kwargs):
        """تحديث حالة المشروع عند الحذف"""
        
        if self.is_cancelled:
            self.status = 'cancelled'
        super().save(*args, **kwargs)


