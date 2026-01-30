from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from urllib.parse import urlencode

from .forms import AlunoForm, CursoForm, FaculdadeForm
from .models import Aluno, Curso, Faculdade
from apps.usuarios.forms import UserCreateForm

User = get_user_model()


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

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user", "curso")
        q = self.request.GET.get("q", "").strip()
        matricula = self.request.GET.get("matricula", "").strip()
        curso = self.request.GET.get("curso", "").strip()
        situacao = self.request.GET.get("situacao", "").strip()

        if q:
            queryset = queryset.filter(
                Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(user__cpf__icontains=q)
                | Q(user__username__icontains=q)
            )
        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if curso:
            queryset = queryset.filter(curso_id=curso)
        if situacao:
            queryset = queryset.filter(situacao=situacao)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = urlencode(query_params)
        context["cursos"] = Curso.objects.all()
        context["situacoes"] = Aluno.Situacao.choices
        return context


class AlunoCadastroUsuarioView(LoginRequiredMixin, FormView):
    """Passo 1 do cadastro de aluno: formulário de cadastro de usuário."""
    form_class = UserCreateForm
    template_name = "academico/aluno_cadastro_usuario.html"

    def form_valid(self, form):
        user = form.save()
        return redirect("academico:aluno_create_com_usuario", user_id=user.pk)


class AlunoCreateComUsuarioView(LoginRequiredMixin, CreateView):
    """Passo 2 do cadastro de aluno: formulário de aluno com usuário já definido."""
    model = Aluno
    form_class = AlunoForm
    template_name = "academico/aluno_form.html"
    success_url = reverse_lazy("academico:aluno_list")

    def get(self, request, *args, **kwargs):
        user_id = self.get_user_id()
        if user_id and Aluno.objects.filter(user_id=user_id).exists():
            return redirect("academico:aluno_list")
        return super().get(request, *args, **kwargs)

    def get_user_id(self):
        return self.kwargs.get("user_id")

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.get_user_id()
        if user_id:
            initial["user"] = user_id
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.get_user_id()
        if user_id:
            kwargs["initial"] = kwargs.get("initial", {})
            kwargs["initial"]["user"] = user_id
            kwargs["user_preenchido_id"] = user_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.get_user_id()
        if user_id:
            context["usuario_cadastrado"] = get_object_or_404(User, pk=user_id)
        return context

    def form_valid(self, form):
        # Garante que o aluno seja vinculado ao usuário da URL (passo 1 do cadastro)
        user_id = self.get_user_id()
        if user_id:
            form.instance.user_id = user_id
        return super().form_valid(form)


class AlunoDetailView(LoginRequiredMixin, DetailView):
    model = Aluno
    context_object_name = "aluno"
    template_name = "academico/aluno_detail.html"


class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    model = Aluno
    form_class = AlunoForm
    template_name = "academico/aluno_form.html"
    success_url = reverse_lazy("academico:aluno_list")
