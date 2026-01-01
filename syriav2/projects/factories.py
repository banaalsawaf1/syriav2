from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from .models import Project
import folium 

class ProjectFactory(ABC):
    """Abstract Factory for creating projects"""
    
    @abstractmethod
    def create_project(self, data, created_by):
        pass
    
    @abstractmethod
    def validate_project(self, data):
        pass
    
    @staticmethod
    def get_factory(project_type):
        """Factory Method to get appropriate factory"""
        factories = {
            'comprehensive': ComprehensiveProjectFactory(),
            'community': CommunityProjectFactory(),
            'development': DevelopmentProjectFactory()
        }
        return factories.get(project_type)


class ComprehensiveProjectFactory(ProjectFactory):
    """Factory for comprehensive reconstruction projects"""
    
    def validate_project(self, data):
        required_fields = ['damage_type', 'area']
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"حقل {field} مطلوب للمشاريع الشاملة")
        
        
        if not all([data.get(f'image{i}') for i in range(1, 5)]):
            raise ValidationError("يجب رفع 4 صور للمشاريع الشاملة")
        
        return True
    
    def create_project(self, data, created_by):
        project = Project(
            name=data['name'],
            project_type='comprehensive',
            description=data['description'],
            damage_type=data['damage_type'],
            address=data['address'],
            governorate=data['governorate'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            estimated_cost=data['estimated_cost'],
            duration=data['duration'],
            area=data['area'],
            created_by=created_by
        )
        
        
        for i in range(1, 5):
            image_field = f'image{i}'
            if data.get(image_field):
                setattr(project, image_field, data[image_field])
        
        return project


class CommunityProjectFactory(ProjectFactory):
    """Factory for community support projects"""
    
    def validate_project(self, data):
        required_fields = ['damage_type']
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"حقل {field} مطلوب للمشاريع المجتمعية")
        
        return True
    
    def create_project(self, data, created_by):
        project = Project(
            name=data['name'],
            project_type='community',
            description=data['description'],
            damage_type=data['damage_type'],
            address=data['address'],
            governorate=data['governorate'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            estimated_cost=data['estimated_cost'],
            duration=data['duration'],
            created_by=created_by
        )
        
        
        for i in range(1, 5):
            image_field = f'image{i}'
            if data.get(image_field):
                setattr(project, image_field, data[image_field])
        
        return project


class DevelopmentProjectFactory(ProjectFactory):
    """Factory for new construction development projects"""
    
    def validate_project(self, data):
        required_fields = ['area']
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"حقل {field} مطلوب للمشاريع الإنشائية")
        
        return True
    
    def create_project(self, data, created_by):
        project = Project(
            name=data['name'],
            project_type='development',
            description=data['description'],
            address=data['address'],
            governorate=data['governorate'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            estimated_cost=data['estimated_cost'],
            duration=data['duration'],
            area=data['area'],
            created_by=created_by
        )
        
        
        if data.get('damage_type'):
            project.damage_type = data['damage_type'] 

        
        for i in range(1, 5):
            image_field = f'image{i}'
            if data.get(image_field):
                setattr(project, image_field, data[image_field])
        
        return project
    
    
class MapFactory:
    """Factory لإنشاء خرائط حسب نوع المشروع"""
    
    @staticmethod
    def create_map(project):
        if not project.latitude or not project.longitude:
            return None
        
        
        marker_color = MapFactory.get_marker_color(project)
        
        
        m = folium.Map(
            location=[float(project.latitude), float(project.longitude)],
            zoom_start=15,
            tiles='OpenStreetMap'
        )
        
        
        folium.Marker(
            [float(project.latitude), float(project.longitude)],
            popup=f'<b>{project.name}</b><br>{project.get_project_type_display()}',
            tooltip='موقع المشروع',
            icon=folium.Icon(color=marker_color, icon='info-sign', prefix='fa')
        ).add_to(m)
        
        return m
    
    @staticmethod
    def get_marker_color(project):
        """الحصول على لون المؤشر حسب نوع المشروع والضرر"""
        if project.project_type == 'development':
            return '#2b6b42'  
        elif project.damage_type == 'total':
            return '#dc3545'  
        elif project.damage_type == 'partial':
            return '#fd7e14'  
        else:
            return '#2b6b42'  