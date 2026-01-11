from django import forms
from .models import ProjectStageUpdate
from projects.models import Project
from accounts.models import User

class ProjectStageUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectStageUpdate
        fields = [
            'project', 'stage_number', 'stage_name', 'stage_description',
            'completion_percentage', 'field_image', 'report_pdf',
            'remaining_cost', 'remaining_duration'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control' , 'required': 'required'}),
            'stage_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 7 , 'required': 'required'}),
            'stage_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'stage_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'required'}),
            'completion_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'required': 'required'}),
            'field_image': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),
            'report_pdf': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'required': 'required'}),
            'remaining_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'remaining_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 3 أشهر', 'required': 'required'}),
        }
        labels = {
            'project': 'اختر المشروع',
            'stage_number': 'رقم المرحلة',
            'stage_name': 'اسم المرحلة',
            'stage_description': 'شرح المرحلة',
            'completion_percentage': 'نسبة إنجاز هذه المرحلة (%)',
            'field_image': 'اختر صورة ميدانية',
            'report_pdf': 'ارفع تقرير PDF لهذه المرحلة',
            'remaining_cost': 'الكلفة المادية المتبقية (بالدولار)',
            'remaining_duration': 'المدة المتبقية لإنجاز المشروع',
        }

    def __init__(self, *args, **kwargs):
        contractor = kwargs.pop('contractor', None)
        super().__init__(*args, **kwargs)
        if contractor:
            self.fields['project'].queryset = Project.objects.filter(
                contractor=contractor,
                status='in_progress',
                is_cancelled=False
            ) 
        
        self.fields['project'].widget.choices = [
            (p.id, f"{p.name} — الكلفة المادية: ${p.estimated_cost}, المدة: {p.duration}")
            for p in self.fields['project'].queryset
        ]

        for field in self.fields.values():
            field.required = True
