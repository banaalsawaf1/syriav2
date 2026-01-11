from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('update/', views.project_stage_update_view, name='project_stages_update'),
    path('detail/<int:project_id>/', views.project_stages_detail_view, name='project_stages_detail'),
    path('admin/updates/', views.admin_updates_management_view, name='admin_updates_management'),
]
