from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

from base.forms import SignupForm

def home(request):
    if request.user.is_authenticated():
        print("entrou")
        return redirect('key_code')
    else:
        print("entrou2")
        hour = datetime.datetime.now().strftime('%H');
        hour = int(hour)
        if hour >= 0 and hour <= 11:
            mensagem = "Bom Dia!"
        elif hour >= 12 and hour <= 17:
            mensagem = "Boa Tarde!"
        else:
            mensagem = "Boa Noite!"
        return render(request, 'copy/home.html', {'mensagem': mensagem})

@login_required
def key_code(request):
    if request.method == 'POST':
        error = True
        return render(request, 'copy/key_code.html', {'error': error})
    else:
        return render(request, 'copy/key_code.html')

def key_cut(request):
    return render(request, 'copy/key_cut.html')

def key_finish(request):
    return render(request, 'copy/key_finish.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password1']
        passwordVerify = request.POST['password2']
        error = "";
        if passwordVerify != password:
            error = "As senhas não conferem "
        if len(password) < 8:
            error = error + "A senha não tem 8 caracteres "
        if len(username) < 1:
            error = error + "Digite o usuário"
        if len(error) == 0:
            user = User.objects.create_user(name, username, password)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            error_bool = True
            information = {
                'error_bool': error_bool,
                'error': error,
            }
            return render(request, 'base/signup.html',information)
    else:
        return render(request, 'base/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = True
            return render(request, 'base/login.html', {'error': error})
    else:
        return render(request, 'base/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
