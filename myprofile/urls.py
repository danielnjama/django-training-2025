from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about-us/',views.about,name='about'),
    path('portfolio/',views.portfolio,name='portfolio'),
    path('blog/',views.blog,name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact-us/',views.contact,name='contact'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    
]