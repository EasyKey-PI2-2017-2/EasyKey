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
    if request.method == 'POST':
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
            error = True
            return render(request, 'copy/key_code.html', {'error': error})
    else:
        error = request.GET.get('error');

        if not error:
            return render(request, 'copy/key_code.html')
        else:
            error = True
            return render(request, 'copy/key_code.html', {'error2': error})

def key_cut(request):
    return render(request, 'copy/key_cut.html')

def key_finish(request):
    return render(request, 'copy/key_finish.html')