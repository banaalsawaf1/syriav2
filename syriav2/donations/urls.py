from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('requests/', views.requests_list, name='requests_list'),
    path('request/<int:pk>/accept/', views.accept_request, name='accept_request'),
    path('request/<int:pk>/reject/', views.reject_request, name='reject_request'),
    path('adopt/<int:pk>/', views.create_adoption_request, name='create_adoption_request'),
    path('adoption-cost/<int:pk>/', views.get_adoption_cost, name='get_adoption_cost'),
    path('donate/<int:pk>/', views.create_donation_request, name='create_donation_request'),
]
