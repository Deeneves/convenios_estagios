from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
import math

from django.db.models import DurationField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from urllib.parse import urlencode

from apps.academico.models import Aluno
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
    model = Aluno
    context_object_name = "alunos_totais"
    template_name = "contrapartida/horas_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("user", "curso")
            .annotate(
                total_horas=Coalesce(
                    Sum("horas__quantidade", output_field=DurationField()),
                    Value(timedelta(0), output_field=DurationField()),
                    output_field=DurationField(),
                )
            )
        )
        aluno = self.request.GET.get("aluno", "").strip()
        matricula = self.request.GET.get("matricula", "").strip()
        curso = self.request.GET.get("curso", "").strip()
        if aluno:
            for termo in aluno.split():
                queryset = queryset.filter(
                    Q(user__first_name__icontains=termo)
                    | Q(user__last_name__icontains=termo)
                    | Q(user__username__icontains=termo)
                )
        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if curso:
            queryset = queryset.filter(curso_id=curso)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = urlencode(query_params)
        context["alunos"] = Aluno.objects.select_related("user").order_by("user__first_name", "user__username")
        context["cursos"] = Aluno.objects.select_related("curso").values("curso_id", "curso__nome").distinct().order_by("curso__nome")
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


class HorasAlunoListView(LoginRequiredMixin, ListView):
    model = Horas
    context_object_name = "registros"
    template_name = "contrapartida/horas_aluno_list.html"
    paginate_by = 15

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("aluno", "aluno__user", "responsavel_registro")
            .filter(aluno_id=self.kwargs.get("aluno_id"))
            .order_by("-data_registro")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno_id = self.kwargs.get("aluno_id")
        aluno = Aluno.objects.select_related("user", "curso").filter(pk=aluno_id).first()
        context["aluno"] = aluno
        total = self.get_queryset().aggregate(
            total=Coalesce(
                Sum("quantidade", output_field=DurationField()),
                Value(timedelta(0), output_field=DurationField()),
                output_field=DurationField(),
            )
        )
        total_td = total["total"] or timedelta(0)
        total_horas = total_td.total_seconds() / 3600
        anos = 0
        if aluno and aluno.curso and aluno.curso.duracao:
            anos = math.ceil(aluno.curso.duracao / 2)
        progresso = []
        restante = total_horas
        for ano in range(1, anos + 1):
            feito = min(100, restante)
            restante = max(0, restante - feito)
            falta = max(0, 100 - feito)
            progresso.append(
                {
                    "ano": ano,
                    "feito": feito,
                    "falta": falta,
                    "percentual": min(100, (feito / 100) * 100 if 100 else 0),
                }
            )
        context["progresso_horas"] = progresso
        context["total_horas"] = total_horas
        context["total_necessario"] = anos * 100
        context["total_restante"] = max(0, (anos * 100) - total_horas)
        return context


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
