from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/update/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('role/<str:role>/', views.users_by_role, name='users_by_role'),
]