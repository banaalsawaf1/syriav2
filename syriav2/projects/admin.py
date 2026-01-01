from django.contrib import admin
from django.utils.html import format_html
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project_type', 'governorate', 'damage_type', 
                    'status', 'created_by', 'created_at', 'image_preview')
    list_filter = ('project_type', 'status', 'governorate', 'damage_type', 'created_at')
    search_fields = ('name', 'description', 'address')
    list_per_page = 20
    readonly_fields = ('created_by', 'created_at', 'updated_at', 'image_previews')
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'project_type', 'description', 'status')}),
        ('الموقع والضرر', {
            'fields': ('damage_type', 'address', 'governorate', 'latitude', 'longitude')
        }),
        ('الصور', {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image_previews')
        }),
        ('المعلومات الإضافية', {
            'fields': ('estimated_cost', 'duration', 'priority_score')
        }),
        ('معلومات النظام', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """عرض معاينة للصورة في قائمة الإدارة"""
        if obj.image1:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image1.url)
        return "لا توجد صورة"
    image_preview.short_description = 'معاينة'
    
    def image_previews(self, obj):
        """عرض جميع صور المشروع في صفحة التعديل"""
        images = obj.get_project_images()
        if images:
            html = '<div style="display: flex; gap: 10px;">'
            for img_url in images:
                html += f'<img src="{img_url}" width="100" height="100" style="border-radius: 5px; border: 1px solid #ddd;" />'
            html += '</div>'
            return format_html(html)
        return "لا توجد صور"
    image_previews.short_description = 'معاينة الصور'
    
    def save_model(self, request, obj, form, change):
        """حفظ منشئ المشروع تلقائياً"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)