# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        }),
        validators=[MinLengthValidator(8, message='كلمة المرور يجب أن تكون على الأقل 8 أحرف')]
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_role'
                
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
       
        self.fields['username'].label = ''
        self.fields['phone_number'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['role'].label = ''
        
        
        self.fields['role'].choices = [
            choice for choice in self.fields['role'].choices 
            if choice[0] != 'system_admin'
        ]
        
        
        self.fields['document'] = forms.ImageField(
            required=False,
            widget=forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_document'
            })
        )
        self.fields['document'].label = ''

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''