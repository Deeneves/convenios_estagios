from django.urls import path
from . import views

urlpatterns = [
    #TODO: Adicionar URLs para o app de usuários
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('usuarios/', views.user_admin_list, name='user_admin_list'),
    path('usuarios/cadastrar/', views.user_admin_create, name='user_admin_create'),
    path('usuarios/<int:pk>/', views.user_admin_detail, name='user_admin_detail'),
    path('usuarios/<int:pk>/editar/', views.user_admin_edit, name='user_admin_edit'),
    path('usuarios/<int:pk>/toggle-ativo/', views.user_admin_toggle_active, name='user_admin_toggle_active'),
]
