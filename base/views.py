from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

from .models import Key


def home(request):
    if request.user.is_authenticated():
        return redirect('key_code')
    else:
        hour = datetime.datetime.now().strftime('%H');
        hour = int(hour)
        message = hello_msg(hour)

        return render(request, 'copy/home.html', {'message': message})


@login_required(login_url='login')
def key_code(request):
    if request.method == 'POST':
        key = Key()
        key.load_key()
        key.load_templates()
        match = key.verify_key_model()
        
        if match:
            key.define_contour()
            key.define_scale()
            key.gcode()
            
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


@login_required(login_url='login')
def key_cut(request):
    return render(request, 'copy/key_cut.html')


@login_required(login_url='login')
def key_finish(request):
    return render(request, 'copy/key_finish.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password1']
        password_verify = request.POST['password2']
        
        error = validate_signup(username, password, password_verify);
        
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


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    
    return redirect('home')


def hello_msg(hour):
    if hour >= 0 and hour <= 11:
        message = "Bom Dia!"
    elif hour >= 12 and hour <= 17:
        message = "Boa Tarde!"
    else:
        message = "Boa Noite!"

    return message


def validate_signup(username, password, password_verify):
    error = ""
    
    if password_verify != password:
        error = "- As senhas não conferem "
    if len(password) < 8:
        error = error + "- A senha não tem 8 caracteres "
    if len(username) < 3:
        error = error + "- Digite o usuário maior que 3 caracteres "
    if password.isdigit():
        error = error + "- A senha possui apenas dígitos "
        
    return error
