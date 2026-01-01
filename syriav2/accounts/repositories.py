from django.core.exceptions import ObjectDoesNotExist
from .models import User


class UserRepository:
    
    @staticmethod
    def get_by_id(user_id):
        """الحصول على مستخدم بالـ ID"""
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_username(username):
        """الحصول على مستخدم بالاسم"""
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_all():
        """الحصول على جميع المستخدمين"""
        return User.objects.all()
    
    @staticmethod
    def get_by_role(role):
        """الحصول على مستخدمين حسب الدور"""
        return User.objects.filter(role=role)
    
    @staticmethod
    def create_user(username, password, phone_number, role, document=None):
        """إنشاء مستخدم جديد"""
        user = User.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            role=role,
            document=document
        )
        return user
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """تحديث بيانات مستخدم"""
        user = UserRepository.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """حذف مستخدم"""
        user = UserRepository.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False
