from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.forms import SignupForm


def home(request):
    if request.user.is_authenticated():
        return render(request, 'copy/step1.html')
    else:
        return render(request, 'copy/step0.html')

def step1(request):
    return render(request, 'copy/step1.html')

def step2(request):
    return render(request, 'copy/step2.html')

def step3(request):
    return render(request, 'copy/step3.html')

def step4(request):
    return render(request, 'copy/step4.html')

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
