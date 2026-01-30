from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.utils.http import url_has_allowed_host_and_scheme

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
    return render(request, 'home.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')