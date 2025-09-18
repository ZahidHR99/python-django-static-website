from django.urls import path
from . import views

# pages

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('hire/', views.hire, name='hire'),
    path('contact/', views.contact, name='contact'),    
]
