from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from .forms import LoginForm, AdminUserCreateForm, AdminUserUpdateForm
from .models import User
from django.utils.http import url_has_allowed_host_and_scheme

from apps.academico.models import Aluno, Curso, Faculdade

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.POST.get('next', '')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('home')
    else:
        form = LoginForm(request)
    next_url = request.POST.get('next', '') if request.method == 'POST' else request.GET.get('next', '')
    return render(request, 'registration/login.html', {'form': form, 'next': next_url})

@login_required
def home(request):
    role_template = {
        User.Role.DIRETOR: 'dashboard/diretor_home.html',
        User.Role.ADMINISTRATIVO: 'dashboard/administrativo_home.html',
        User.Role.ALUNO: 'dashboard/aluno_home.html',
        User.Role.SECRETARIA: 'dashboard/secretaria_home.html',
    }
    template = role_template.get(request.user.role, 'dashboard/aluno_home.html')
    context = {}
    if request.user.role == User.Role.DIRETOR:
        cursos = (
            Curso.objects.annotate(alunos_total=Count("alunos"))
            .order_by("nome")
        )
        context = {
            "alunos_count": Aluno.objects.count(),
            "cursos_count": Curso.objects.count(),
            "faculdades_count": Faculdade.objects.count(),
            "cursos_labels": [curso.nome for curso in cursos],
            "cursos_values": [curso.alunos_total for curso in cursos],
        }
    return render(request, template, context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


def _is_diretor_or_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.role == User.Role.DIRETOR)


def diretor_or_superuser_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not _is_diretor_or_superuser(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


@login_required
@diretor_or_superuser_required
def user_admin_list(request):
    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()

    users = User.objects.all().order_by("first_name", "last_name", "cpf")
    if query:
        users = users.filter(
            Q(cpf__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
    if role:
        users = users.filter(role=role)

    return render(
        request,
        "usuarios/usuario_list.html",
        {"users": users, "roles": User.Role.choices},
    )


@login_required
@diretor_or_superuser_required
def user_admin_create(request):
    if request.method == "POST":
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect("user_admin_list")
    else:
        form = AdminUserCreateForm()

    return render(request, "usuarios/usuario_form.html", {"form": form})


@login_required
@diretor_or_superuser_required
def user_admin_detail(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    return render(request, "usuarios/usuario_detail.html", {"user_item": user_item})


@login_required
@diretor_or_superuser_required
def user_admin_edit(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = AdminUserUpdateForm(request.POST, instance=user_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("user_admin_list")
    else:
        form = AdminUserUpdateForm(instance=user_item)

    return render(
        request,
        "usuarios/usuario_edit.html",
        {"form": form, "user_item": user_item},
    )


@login_required
@diretor_or_superuser_required
def user_admin_toggle_active(request, pk):
    if request.method != "POST":
        return redirect("user_admin_list")
    user_item = get_object_or_404(User, pk=pk)
    user_item.is_active = not user_item.is_active
    user_item.save(update_fields=["is_active"])
    status = "ativado" if user_item.is_active else "desativado"
    messages.success(request, f"Usuário {status} com sucesso.")
    return redirect("user_admin_list")
