from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from urllib.parse import urlencode

from apps.academico.models import Aluno
from apps.usuarios.models import User
from .forms import EncaminhamentoForm, HorasForm, SecretariaForm
from .models import Encaminhamento, Horas, Secretaria

# --- Secretaria ---
class SecretariaListView(LoginRequiredMixin, ListView):
    model = Secretaria
    context_object_name = "secretarias"
    template_name = "contrapartida/secretaria_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(Q(nome__icontains=q) | Q(sigla__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = urlencode(query_params)
        return context


class SecretariaCreateView(LoginRequiredMixin, CreateView):
    model = Secretaria
    form_class = SecretariaForm
    template_name = "contrapartida/secretaria_form.html"
    success_url = reverse_lazy("contrapartida:secretaria_list")


class SecretariaDetailView(LoginRequiredMixin, DetailView):
    model = Secretaria
    context_object_name = "secretaria"
    template_name = "contrapartida/secretaria_detail.html"


class SecretariaUpdateView(LoginRequiredMixin, UpdateView):
    model = Secretaria
    form_class = SecretariaForm
    template_name = "contrapartida/secretaria_form.html"
    success_url = reverse_lazy("contrapartida:secretaria_list")


class SecretariaDeleteView(LoginRequiredMixin, DeleteView):
    model = Secretaria
    context_object_name = "secretaria"
    template_name = "contrapartida/secretaria_confirm_delete.html"
    success_url = reverse_lazy("contrapartida:secretaria_list")


# --- Encaminhamento ---
class EncaminhamentoListView(LoginRequiredMixin, ListView):
    model = Encaminhamento
    context_object_name = "encaminhamentos"
    template_name = "contrapartida/encaminhamento_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related("secretaria", "aluno", "responsavel_emissao", "aluno__user")
        numero = self.request.GET.get("numero", "").strip()
        aluno = self.request.GET.get("aluno", "").strip()
        secretaria = self.request.GET.get("secretaria", "").strip()
        data = self.request.GET.get("data", "").strip()
        if numero:
            queryset = queryset.filter(numero=numero)
        if aluno:
            queryset = queryset.filter(aluno_id=aluno)
        if secretaria:
            queryset = queryset.filter(secretaria_id=secretaria)
        if data:
            queryset = queryset.filter(data=data)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = urlencode(query_params)
        context["alunos"] = Aluno.objects.select_related("user").order_by("user__first_name", "user__username")
        context["secretarias"] = Secretaria.objects.all()
        return context


class EncaminhamentoCreateView(LoginRequiredMixin, CreateView):
    model = Encaminhamento
    form_class = EncaminhamentoForm
    template_name = "contrapartida/encaminhamento_form.html"
    success_url = reverse_lazy("contrapartida:encaminhamento_list")

    def form_valid(self, form):
        form.instance.data = timezone.localdate()
        form.instance.responsavel_emissao = self.request.user
        return super().form_valid(form)


class EncaminhamentoDetailView(LoginRequiredMixin, DetailView):
    model = Encaminhamento
    context_object_name = "encaminhamento"
    template_name = "contrapartida/encaminhamento_detail.html"


class EncaminhamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Encaminhamento
    form_class = EncaminhamentoForm
    template_name = "contrapartida/encaminhamento_form.html"
    success_url = reverse_lazy("contrapartida:encaminhamento_list")


class EncaminhamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Encaminhamento
    context_object_name = "encaminhamento"
    template_name = "contrapartida/encaminhamento_confirm_delete.html"
    success_url = reverse_lazy("contrapartida:encaminhamento_list")


# --- Horas ---
class HorasListView(LoginRequiredMixin, ListView):
    model = Horas
    context_object_name = "horas"
    template_name = "contrapartida/horas_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related("aluno", "responsavel_registro", "aluno__user")
        aluno = self.request.GET.get("aluno", "").strip()
        responsavel = self.request.GET.get("responsavel", "").strip()
        data = self.request.GET.get("data_registro", "").strip()
        if aluno:
            queryset = queryset.filter(aluno_id=aluno)
        if responsavel:
            queryset = queryset.filter(responsavel_registro_id=responsavel)
        if data:
            queryset = queryset.filter(data_registro=data)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = urlencode(query_params)
        context["alunos"] = Aluno.objects.select_related("user").order_by("user__first_name", "user__username")
        context["responsaveis"] = User.objects.order_by("first_name", "username")
        return context


class HorasCreateView(LoginRequiredMixin, CreateView):
    model = Horas
    form_class = HorasForm
    template_name = "contrapartida/horas_form.html"
    success_url = reverse_lazy("contrapartida:horas_list")

    def form_valid(self, form):
        form.instance.data_registro = timezone.localdate()
        form.instance.responsavel_registro = self.request.user
        return super().form_valid(form)


class HorasDetailView(LoginRequiredMixin, DetailView):
    model = Horas
    context_object_name = "registro_horas"
    template_name = "contrapartida/horas_detail.html"


class HorasUpdateView(LoginRequiredMixin, UpdateView):
    model = Horas
    form_class = HorasForm
    template_name = "contrapartida/horas_form.html"
    success_url = reverse_lazy("contrapartida:horas_list")


class HorasDeleteView(LoginRequiredMixin, DeleteView):
    model = Horas
    context_object_name = "registro_horas"
    template_name = "contrapartida/horas_confirm_delete.html"
    success_url = reverse_lazy("contrapartida:horas_list")
