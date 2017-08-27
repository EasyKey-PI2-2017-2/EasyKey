from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Home")


def login(request):
    return HttpResponse("Login")


def signup(request):
    return HttpResponse("Cadastro")
