from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/weather/', views.get_weather, name='get_weather'),
    path('api/forecast/', views.get_forecast, name='get_forecast'),
]