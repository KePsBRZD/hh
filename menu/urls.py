from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('draw/', views.draw_menu, name='draw_menu'),
    path('about/', views.about, name='about'),
]