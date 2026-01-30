from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import User
from django.utils.http import url_has_allowed_host_and_scheme

from django.db.models import Count

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
