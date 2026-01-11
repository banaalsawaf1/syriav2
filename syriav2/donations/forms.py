from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, Div
from crispy_forms.bootstrap import FormActions
from django.db.models import Sum
from .models import DonationRequest

class DonationRequestForm(forms.ModelForm):
    """نموذج لطلب التبرع (سيكون للمنظمة والمواطن)"""
    class Meta:
        model = DonationRequest
        fields = ['project', 'adoption_type', 'amount', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        
        if self.user and self.user.role == 'organization':
            self.fields['adoption_type'].required = True
            self.fields['amount'].required = True
       
        elif self.user and self.user.role == 'citizen':
            
            self.fields['donation_amount'] = forms.DecimalField(
                max_digits=15, decimal_places=2,
                label='مبلغ التبرع',
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
            
            del self.fields['adoption_type']
            del self.fields['amount']

            
class AdoptionForm(forms.ModelForm):
    confirm = forms.BooleanField(
        required=True,
        label="نعم، أنا متأكد",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'يجب تأكيد الطلب'}
    )
   
    display_amount = forms.CharField(
        required=False,
        label="المبلغ المقدر",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa;'
        })
    )
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'adoption-form'
        
       
        self.helper.layout = Layout(
            HTML('<h2 class="form-title">تبني المشروع</h2>'),
            
            HTML(f'<div class="alert alert-info text-center" style="font-size: 16px;">'
                 f'<i class="fas fa-info-circle me-2"></i>'
                 f'المشروع: <strong>{self.project.name}</strong> | '
                 f'</div>'),
            
            'adoption_type',
            
           
            HTML('<div class="form-group" id="amount-display-field" style="display: none;">'
                 '<label for="display_amount">المبلغ المقدر *</label>'
                 '<input type="text" id="display_amount" class="form-control" readonly>'
                 '</div>'),

            Div(
                HTML('<div id="cost-info" class="alert alert-warning text-center" style="display: none;"></div>'),
                css_class='form-group'
            ),
            
            Div(
                Field('confirm', css_class='form-check-input'),
                css_class='form-group',
                css_id='confirm-field'
            ),
            
           
            HTML('<input type="hidden" name="amount" id="id_amount">'),
            
            FormActions(
                Submit('submit', 'تبني المشروع', css_class='btn btn-primary btn-lg'),
                HTML(f'<a href="/projects/{self.project.pk}/" class="btn btn-secondary btn-lg">إلغاء والعودة</a>')
            )
        )
        
        
      
    
        
        
        self.fields['adoption_type'].choices = [('', 'اختر نوع التبني'), ('full', 'كامل'), ('partial', 'جزئي')]
        self.fields['adoption_type'].label = 'اختيار نوع التبني *'
        self.fields['adoption_type'].widget.attrs.update({
            'class': 'form-control',
            'id': 'id_adoption_type',
            'required': 'required'
        })
    
    class Meta:
        model = DonationRequest
        fields = ['adoption_type', 'amount', 'confirm']
        widgets = {
            'adoption_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'adoption_type': 'اختيار نوع التبني *',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        adoption_type = cleaned_data.get('adoption_type')
        
        if not adoption_type:
            raise forms.ValidationError("الرجاء اختيار نوع التبني")
        

        
    
        current_funding = DonationRequest.objects.filter(
        project=self.project,
        request_type='organization',
        status='accepted'
        ).aggregate(total=Sum('amount'))['total'] or 0
    
        remaining_cost = self.project.estimated_cost - current_funding

        
        if adoption_type == 'full':
            if remaining_cost < self.project.estimated_cost:
             raise forms.ValidationError("لا يمكن التبني الكامل لأن جزءًا من المشروع مُموَّل بالفعل.")
            cleaned_data['amount'] = self.project.estimated_cost
            self.cost_message = f'سيتم دفع كامل المبلغ ${self.project.estimated_cost:,} هل أنت متأكد؟'
        elif adoption_type == 'partial':
            half_cost = self.project.estimated_cost / 2
            if remaining_cost < half_cost:
              raise forms.ValidationError("لا يمكن التبني الجزئي لأن التمويل المتبقي أقل من نصف الكلفة.")
            cleaned_data['amount'] = half_cost
            self.cost_message = f'سيتم دفع نصف المبلغ ${half_cost:,} هل أنت متأكد؟'
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.request_type = 'organization'
        instance.project = self.project
        instance.organization = self.user
        instance.status = 'pending'
        instance.confirmation = self.cleaned_data['confirm']
        
        
        instance.amount = self.cleaned_data.get('amount', 0)
        
        if commit:
            instance.save()
        
        return instance

            
class DonationForm(forms.ModelForm):
    donor_name = forms.CharField(
        max_length=100,
        required=False,
        label="اسم المُتَبَرِّع",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسمك أو اتركه فارغًا ليكون "مجهول"'
        })
    )
    
    donation_amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=1,
        label="المبلغ (بالدولار الأمريكي)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل المبلغ بالدولار، مثال: 500'
        })
    )

    class Meta:
        model = DonationRequest
        fields = ['donation_amount' ]  
        

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.request_type = 'citizen'
        instance.project = self.project
        instance.citizen = self.user
        instance.status = 'pending'
        
        donor_name = self.cleaned_data.get('donor_name', '').strip()
        if not donor_name:
            donor_name = 'مجهول'
        instance.message = f"اسم المُتبرع: {donor_name}\n" + (instance.message or "")
        if commit:
            instance.save()
        return instance
