from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='draw-home'),
    path('drawing-result/', views.drawingResult, name='draw-drawing-result')
]