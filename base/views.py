from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from base.forms import SignupForm


def home(request):
    if request.user.is_authenticated():
        user = User.objects.get(first_name=request.user.first_name)
        print(user)
        return render(request, 'copy/key_code.html')
    else:
        return render(request, 'copy/home.html')


@login_required
def key_code(request):
    print(request.user)
    print(request.method)
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
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'base/signup.html', {'form': form})
