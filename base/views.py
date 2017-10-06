from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

from base.forms import SignupForm
from chave.views import Chave

def home(request):
    if request.user.is_authenticated():
        return redirect('key_code')
    else:
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
        chave = Chave()
        chave.carregar_chave()
        chave.carregar_templates()
        match = chave.verificar_modelo()
        if match:
            chave.definir_escala()
            chave.definir_contorno()
            chave.gcode()
            return redirect('key_cut')
        else:
            return render(request, 'copy/key_code.html', {'match': match})

    else:
        return render(request, 'copy/key_code.html')

@login_required
def key_cut(request):
    return render(request, 'copy/key_cut.html')

@login_required
def key_finish(request):
    return render(request, 'copy/key_finish.html')

@login_required
def signup(request):
    if request.method == 'POST':
        name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password1']
        passwordVerify = request.POST['password2']
        error = "";
        if passwordVerify != password:
            error = "- As senhas não conferem "
        if len(password) < 8:
            error = error + "- A senha não tem 8 caracteres "
        if len(username) < 1:
            error = error + "- Digite o usuário"
        if password.isdigit():
            error = error + "- A senha possui apenas digitos"
        if len(error) == 0:
            if not User.objects.filter(username = username).exists():
                user = User.objects.create_user(username, name, password)
                user.save()
                login(request, user)
                return redirect('home')
            else:
                error_bool = True
                error = "Já existe uma conta com esse usuário!"
                information = {
                    'error_bool': error_bool,
                    'error': error,
                }
                return render(request, 'base/signup.html', information)
        else:
            error_bool = True
            information = {
                'error_bool': error_bool,
                'error': error,
            }
            return render(request, 'base/signup.html', information)
    else:
        return render(request, 'base/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = True
            return render(request, 'base/login.html', {'error': error})
    else:
        return render(request, 'base/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
