from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect, name='detect'),
    path('history/', views.history, name='history'),
    path('history/delete/<int:pk>/', views.delete_history, name='delete_history'),
    path('about/', views.about, name='about'),
    # Legacy URL for backward compatibility
    path('upload/', views.upload_video, name='upload_video'),
]
