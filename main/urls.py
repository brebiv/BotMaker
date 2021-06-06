from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Lander page"),
    path('dashboard/', views.dashboard, name="Dashboard"),
]
