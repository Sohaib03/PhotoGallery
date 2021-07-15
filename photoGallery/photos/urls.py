from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:key>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
]
