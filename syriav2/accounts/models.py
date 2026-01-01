from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('citizen', 'مواطن'),
        ('organization', 'منظمة'),
        ('contractor', 'متعهد'),
        ('system_admin', 'مدير النظام'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    document = models.ImageField(upload_to='user_documents/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name='محذوف نهائياً')
    
    def save(self, *args, **kwargs):
        
        if self.role == 'citizen':
            self.document = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
