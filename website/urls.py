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
    path('api/demo1/', views.demo1, name='demo1'),   
    path('api/demo2/', views.demo2, name='demo2'),   
    path('api/demo3/', views.demo3, name='demo3'),  
    path('api/demo4/', views.demo4, name='demo4'),  
    path('api/demo5/', views.demo5, name='demo5'),  
    path('api/demo6/', views.demo6, name='demo6'),  
    path('api/demo7/', views.demo7, name='demo7'), 
    path('api/demo8/', views.demo8, name='demo8'), 
    path('api/demo9/', views.demo9, name='demo9'), 
    path('api/download/', views.download, name='download'), 
    path('api/binary_response/', views.binary_response, name='binary_response'), 
]
