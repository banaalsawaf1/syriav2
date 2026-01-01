from django.core.management.base import BaseCommand
from accounts.models import User
import os

class Command(BaseCommand):
    help = 'إنشاء حساب مدير النظام المسبق'
    
    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD')
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                password=password,
                role='system_admin',
                phone_number='+963XXXXXXXXX',  
                is_staff=True,      
                is_superuser=True,  
            )
            self.stdout.write(self.style.SUCCESS(f'تم إنشاء حساب مدير النظام: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'الحساب {username} موجود بالفعل'))
