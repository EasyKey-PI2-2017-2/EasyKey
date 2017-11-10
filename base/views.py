from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
import datetime
import random
import string

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
            return redirect('key_payment')
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
    chave = Chave()
    chave.enviar_comandos()
    return render(request, 'copy/key_cut.html')

def key_finish(request):
    return render(request, 'copy/key_finish.html')

def key_payment(request):
    # What you want tha button to do.
    ale = random.randint(1,100)
    paypal_dict = {
        "business": "mdiebr-facilitator@gmail.com",
        "amount": "{}".format(ale),
        "item_name": "Cópia de chave - Teste {}".format(ale),
        "invoice": "{}".format(''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(15))),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('key_cut')),
        "cancel_return": request.build_absolute_uri(reverse('home')),
        "custom": "premium_plan",
        "currency_code": "BRL",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "copy/key_payment.html", context)