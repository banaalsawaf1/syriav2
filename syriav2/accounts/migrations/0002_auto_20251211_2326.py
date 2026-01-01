from django.db import migrations
from django.contrib.auth.hashers import make_password
import os

def create_system_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    
    
    if not User.objects.filter(username=os.environ.get('ADMIN_USERNAME')).exists():
        User.objects.create(
            username = os.environ.get('ADMIN_USERNAME'),
            password = os.environ.get('ADMIN_PASSWORD'),
            role='system_admin',
            phone_number='+963123456789',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

def delete_system_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(username=os.environ.get('ADMIN_USERNAME')).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_system_admin, delete_system_admin),
    ]