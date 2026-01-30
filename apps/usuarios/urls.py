from django.urls import path
from . import views

urlpatterns = [
    #TODO: Adicionar URLs para o app de usuários
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
]