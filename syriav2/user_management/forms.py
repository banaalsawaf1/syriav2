from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, Div
from crispy_forms.bootstrap import FormActions
from accounts.models import User

class UserCreateForm(UserCreationForm):
    """نموذج إضافة مستخدم جديد من قبل المدير"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'user-form'
        
        
        self.helper.layout = Layout(
            HTML('<h2 class="form-title">إضافة مستخدم جديد</h2>'),
            
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('phone_number', css_class='form-group col-md-6'),
            ),
            
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            
            'role',
            
            
            Div(
                Field('document', css_class='form-control'),
                css_class='form-group',
                css_id='document-field',
                style='display:none;'
            ),
            
            FormActions(
                Submit('submit', 'إضافة المستخدم', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "user_management:user_list" %}" class="btn btn-secondary btn-lg">إلغاء</a>')
            )
        )
        
        
        self.fields['document'] = forms.ImageField(
            required=False,
            widget=forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_document'
            }),
            label="الوثيقة"
        )
        self.fields['password1'].label = 'كلمة المرور'
        self.fields['password2'].label = 'تأكيد كلمة المرور'
        
        self.fields['role'].choices = [
            choice for choice in self.fields['role'].choices
            if choice[0] != 'system_admin'
        ]
    
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'role', 'password1', 'password2', 'document']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المستخدم'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهاتف'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_role'
            }),
        }
        
        labels = {
            'username': 'اسم المستخدم *',
            'phone_number': 'رقم الهاتف *',
            'role': 'الدور *',
            'password1': 'كلمة المرور *',
            'password2': 'تأكيد كلمة المرور *',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        document = cleaned_data.get('document')
        
        
        if role in ['organization', 'contractor'] and not document:
            raise ValidationError("الوثيقة مطلوبة للمنظمة والمتعهد")
        
        return cleaned_data

class UserEditForm(forms.ModelForm):
    """نموذج تعديل مستخدم"""
    
    new_password1 = forms.CharField(
        label="كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور الجديدة (اترك فارغاً إذا لم ترد التغيير)'
        }),
        required=False
    )
    
    new_password2 = forms.CharField(
        label="تأكيد كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تأكيد كلمة المرور الجديدة'
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'user-form'
        
        
        self.fields['document'] = forms.ImageField(
            required=False,
            widget=forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_document'
            }),
            label="الوثيقة"
        )
        
        
        self.helper.layout = Layout(
            HTML('<h2 class="form-title">تعديل المستخدم</h2>'),
            
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('phone_number', css_class='form-group col-md-6'),
            ),
            
            'role',
            
            HTML("""
            <div class="form-group">
                <label for="id_new_password1">كلمة المرور الجديدة</label>
                <input type="password" name="new_password1" class="form-control" id="id_new_password1"
                       placeholder="كلمة المرور الجديدة (اترك فارغاً إذا لم ترد التغيير)">
            </div>
            """),
            
            HTML("""
            <div class="form-group">
                <label for="id_new_password2">تأكيد كلمة المرور الجديدة</label>
                <input type="password" name="new_password2" class="form-control" id="id_new_password2"
                       placeholder="تأكيد كلمة المرور الجديدة">
            </div>
            """),
            
            
            HTML("""
            <div class="form-group" id="document-field">
                <label for="id_document">الوثيقة</label>
                <input type="file" name="document" class="form-control" id="id_document">
                <small class="text-muted">
                    {% if form.instance.document %}
                    <a href="{{ form.instance.document.url }}" target="_blank" class="mt-2 d-inline-block">
                        <i class="fas fa-eye me-1"></i>عرض الوثيقة الحالية
                    </a><br>
                    {% endif %}
                    اترك فارغاً للحفاظ على الوثيقة الحالية
                </small>
            </div>
            """),
            
            FormActions(
                Submit('submit', 'تحديث المستخدم', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "user_management:user_list" %}" class="btn btn-secondary btn-lg">إلغاء</a>')
            )
        )
        
        
        self.fields['role'].choices = [
            choice for choice in self.fields['role'].choices
            if choice[0] != 'system_admin'
        ]
    
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المستخدم'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهاتف'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_role'
            }),
        }
        labels = {
            'username': 'اسم المستخدم *',
            'phone_number': 'رقم الهاتف *',
            'role': 'الدور *',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        
        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("كلمات المرور غير متطابقة")
        
        
        if self.instance.role == 'citizen' and role in ['organization', 'contractor']:
            if not self.cleaned_data.get('document') and not self.instance.document:
                raise ValidationError("الوثيقة مطلوبة عند تغيير الدور إلى منظمة أو متعهد")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            user.set_password(new_password1)
        
        
        document = self.cleaned_data.get('document')
        if document:
            user.document = document
        
        if commit:
            user.save()
        
        return user