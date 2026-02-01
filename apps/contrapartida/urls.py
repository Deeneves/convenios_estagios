from django.urls import path
from . import views

app_name = 'contrapartida'

urlpatterns = [
    # Secretaria
    path("secretarias/", views.SecretariaListView.as_view(), name="secretaria_list"),
    path("secretarias/cadastrar/", views.SecretariaCreateView.as_view(), name="secretaria_create"),
    path("secretarias/<int:pk>/", views.SecretariaDetailView.as_view(), name="secretaria_detail"),
    path("secretarias/<int:pk>/editar/", views.SecretariaUpdateView.as_view(), name="secretaria_edit"),
    path("secretarias/<int:pk>/excluir/", views.SecretariaDeleteView.as_view(), name="secretaria_delete"),
    # Encaminhamento
    path("encaminhamentos/", views.EncaminhamentoListView.as_view(), name="encaminhamento_list"),
    path("encaminhamentos/cadastrar/", views.EncaminhamentoCreateView.as_view(), name="encaminhamento_create"),
    path("encaminhamentos/<int:pk>/", views.EncaminhamentoDetailView.as_view(), name="encaminhamento_detail"),
    path("encaminhamentos/<int:pk>/editar/", views.EncaminhamentoUpdateView.as_view(), name="encaminhamento_edit"),
    path("encaminhamentos/<int:pk>/excluir/", views.EncaminhamentoDeleteView.as_view(), name="encaminhamento_delete"),
    # Horas
    path("horas/", views.HorasListView.as_view(), name="horas_list"),
    path("horas/cadastrar/", views.HorasCreateView.as_view(), name="horas_create"),
    path("horas/<int:pk>/", views.HorasDetailView.as_view(), name="horas_detail"),
    path("horas/<int:pk>/editar/", views.HorasUpdateView.as_view(), name="horas_edit"),
    path("horas/<int:pk>/excluir/", views.HorasDeleteView.as_view(), name="horas_delete"),
]
