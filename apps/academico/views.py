from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AlunoForm, CursoForm, FaculdadeForm
from .models import Aluno, Curso, Faculdade


# --- Faculdade ---
class FaculdadeListView(LoginRequiredMixin, ListView):
    model = Faculdade
    context_object_name = "faculdades"
    template_name = "academico/faculdade_list.html"
    paginate_by = 15


class FaculdadeCreateView(LoginRequiredMixin, CreateView):
    model = Faculdade
    form_class = FaculdadeForm
    template_name = "academico/faculdade_form.html"
    success_url = reverse_lazy("academico:faculdade_list")


class FaculdadeDetailView(LoginRequiredMixin, DetailView):
    model = Faculdade
    context_object_name = "faculdade"
    template_name = "academico/faculdade_detail.html"


# --- Curso ---
class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "academico/curso_list.html"
    paginate_by = 15


class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = "academico/curso_form.html"
    success_url = reverse_lazy("academico:curso_list")


class CursoDetailView(LoginRequiredMixin, DetailView):
    model = Curso
    context_object_name = "curso"
    template_name = "academico/curso_detail.html"


# --- Aluno ---
class AlunoListView(LoginRequiredMixin, ListView):
    model = Aluno
    context_object_name = "alunos"
    template_name = "academico/aluno_list.html"
    paginate_by = 15


class AlunoCreateView(LoginRequiredMixin, CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = "academico/aluno_form.html"
    success_url = reverse_lazy("academico:aluno_list")


class AlunoDetailView(LoginRequiredMixin, DetailView):
    model = Aluno
    context_object_name = "aluno"
    template_name = "academico/aluno_detail.html"
