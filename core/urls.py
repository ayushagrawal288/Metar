from django.urls import path
from core import views

urlpatterns = [
    path('ping', views.pingView, name='ping'),
    path('info', views.infoView, name='info')
]
