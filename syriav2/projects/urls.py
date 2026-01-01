from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/update/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:pk>/change-status/', views.project_change_status, name='change_status'),
    path('type/<str:project_type>/', views.projects_by_type, name='project_by_type'),
    path('public/type/<str:project_type>/', views.projects_by_type_public, name='projects_by_type_public'),
    path('<int:pk>/assign-contractor/', views.assign_contractor, name='assign_contractor'),
    path('get-contractors/', views.get_contractors, name='get_contractors'),
]