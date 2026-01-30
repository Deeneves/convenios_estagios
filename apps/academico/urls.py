from django.urls import path
from . import views

app_name = "academico"

urlpatterns = [
    # Faculdade
    path("faculdades/", views.FaculdadeListView.as_view(), name="faculdade_list"),
    path("faculdades/cadastrar/", views.FaculdadeCreateView.as_view(), name="faculdade_create"),
    path("faculdades/<int:pk>/", views.FaculdadeDetailView.as_view(), name="faculdade_detail"),
    # Curso
    path("cursos/", views.CursoListView.as_view(), name="curso_list"),
    path("cursos/cadastrar/", views.CursoCreateView.as_view(), name="curso_create"),
    path("cursos/<int:pk>/", views.CursoDetailView.as_view(), name="curso_detail"),
    # Aluno
    path("alunos/", views.AlunoListView.as_view(), name="aluno_list"),
    path("alunos/cadastrar/<int:user_id>/", views.AlunoCreateComUsuarioView.as_view(), name="aluno_create_com_usuario"),
    path("alunos/cadastrar/", views.AlunoCadastroUsuarioView.as_view(), name="aluno_create"),
    path("alunos/<int:pk>/", views.AlunoDetailView.as_view(), name="aluno_detail"),
]
