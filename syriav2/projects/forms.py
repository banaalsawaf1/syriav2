from django import forms
from django.core.exceptions import ValidationError
from .models import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from crispy_forms.bootstrap import FormActions
from .factories import ProjectFactory

class ProjectForm(forms.ModelForm):
    """نموذج إضافة/تعديل المشروع"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'project-form'
        
        
        self.helper.layout = Layout(
            HTML('<h2 class="form-title">إضافة مشروع جديد</h2>'),
            
            Row(
                Column('project_type', css_class='form-group col-md-6'),
                Column('name', css_class='form-group col-md-6'),
            ),
            
            'description',
            'address',
            
            Row(
                Column('governorate', css_class='form-group col-md-6'),
                Column('damage_type', css_class='form-group col-md-6'),
            ),
            
            HTML('<h4 class="images-title">صور المشروع (4 صور مطلوبة)</h4>'),
            
            Row(
                Column('image1', css_class='form-group col-md-3'),
                Column('image2', css_class='form-group col-md-3'),
                Column('image3', css_class='form-group col-md-3'),
                Column('image4', css_class='form-group col-md-3'),
            ),
            
            HTML('<h4 class="location-title">موقع المشروع على الخريطة</h4>'),
            Row(
                Column('latitude', css_class='form-group col-md-6'),
                Column('longitude', css_class='form-group col-md-6'),
            ),
            
            HTML("""
            <div class="form-group">
                <label for="map">تحديد الموقع على الخريطة:</label>
                <div id="map" style="height: 400px; width: 100%; border-radius: 10px;"></div>
                <small class="text-muted">انقر على الخريطة لتحديد موقع المشروع</small>
            </div>
            """),
           
            Row(
                Column('estimated_cost', css_class='form-group col-md-4'),
                Column('duration', css_class='form-group col-md-4'),
                Column('area', css_class='form-group col-md-4'),
            ),

            FormActions(
                Submit('submit', 'إضافة المشروع', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "projects:project_list" %}" class="btn btn-secondary btn-lg">إلغاء</a>')
            )
        )
    
    class Meta:
        model = Project
        fields = [
            'name', 'project_type', 'description', 'damage_type',
            'address', 'governorate', 'latitude', 'longitude',
            'image1', 'image2', 'image3', 'image4',
    'estimated_cost', 'duration', 'area'  
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المشروع'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل وصفاً تفصيلياً للمشروع',
                'rows': 15
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل العنوان التفصيلي',
                'rows': 1
            }),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'damage_type': forms.Select(attrs={'class': 'form-control'}),
            'governorate': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'خط العرض',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'خط الطول',
                'step': '0.000001'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
            'image4': forms.FileInput(attrs={'class': 'form-control'}),
            
            'estimated_cost': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل التكلفة المادية بالدولار (مثال: 250000)',
            'min': '0' 
            }),  
            'duration': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: 30 يوم أو 6 أشهر'
            }),
            'area': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل المساحة بالمتر المربع',
            'step': '0.01'
             }),
        }
        labels = {
            'name': 'اسم المشروع',
            'project_type': 'نوع المشروع',
            'description': 'وصف تفصيلي عن المشروع',
            'damage_type': 'نوع الضرر*',
            'address': 'العنوان',
            'governorate': 'المحافظة',
            'latitude': 'خط العرض*',
            'longitude': 'خط الطول*',
            'image1': 'الصورة الأولى',
            'image2': 'الصورة الثانية',
            'image3': 'الصورة الثالثة',
            'image4': 'الصورة الرابعة',
            'estimated_cost': "التكلفة المادية للمشروع (بالدولار)",
            'duration': "المدة المقدرة لإنجاز المشروع*",
            'area': "مساحة الموقع (م²)*",
        }
    
    def clean(self):
        """التحقق من صحة البيانات"""
        cleaned_data = super().clean()
        project_type = cleaned_data.get('project_type')
        
        if project_type:
            try:
                
                factory = ProjectFactory.get_factory(project_type)
                factory.validate_project(cleaned_data)
            except ValidationError as e:
                raise forms.ValidationError(e)
        
        return cleaned_data


class ProjectEditForm(ProjectForm):
    """نموذج تعديل المشروع"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[0] = HTML('<h2 class="form-title">تعديل المشروع</h2>')
        self.helper.layout[-1].fields[0] = Submit('submit', 'تحديث المشروع', css_class='btn btn-primary btn-lg')

        
        
        self.fields['image1'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['image4'].required = False

class AssignContractorForm(forms.Form):
    """نموذج تعيين متعهد للمشروع"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from accounts.models import User
        contractors = User.objects.filter(role='contractor',
                                           is_deleted=False
                                          )
        
        
        choices = [('', 'اختر متعهد...')]
        choices += [(contractor.id, contractor.username) for contractor in contractors]
        
        self.fields['contractor'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={
                'class': 'form-control',
                'style': 'border-color: #ffc107; color: #2b6b42;'
            }),
            label="اختر المتعهد:"
        )
    
    def save(self, project):
        """حفظ المتعهد المعين"""
        from accounts.models import User
        contractor_id = self.cleaned_data['contractor']
        if contractor_id:
            contractor = User.objects.get(id=contractor_id)
            project.contractor = contractor
            project.status = 'in_progress'  
            project.save()
            return contractor
        return None