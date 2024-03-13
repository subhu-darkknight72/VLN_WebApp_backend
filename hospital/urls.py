from django.urls import path
from . import views

urlpatterns = [
    path('reset/', views.reset, name='hospitalReset'),
    path('performAction/', views.performAction, name='performAction'),
    path('', views.index, name='hospitalIndex'),
]
