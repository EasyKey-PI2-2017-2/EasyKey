from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
import datetime
import random
import string
import serial
import time

from .models import Key, Payment

ser = None


def serial_connection_required(func):
    def decorator(request, *args, **kwargs):
        global ser

        if not ser:
            message = hello_msg()
            error = True
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
    decorator.__doc__=func.__doc__
    decorator.__name__=func.__name__
    return decorator


def home(request):
    global ser

    message = hello_msg()

    if request.method == 'GET':
        return render(request, 'copy/home.html', {'message': message})
    if request.method == 'POST':
        if not ser:
            try_to_connect()
        if ser:
            return redirect('key_code')
        if not ser:
            error = True
            return render(
                request, 'copy/home.html',
                {'message': message, 'serial_error': error})


@serial_connection_required
def key_code(request):
    global ser

    if request.method == 'POST':
        key = Key()
        key.load_key()
        key.load_templates()
        #match = key.verify_key_model()
        if True:
            key.define_contour()
            key.define_scale()
            key.gcode()
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

@serial_connection_required
def key_cut(request):
    if request.method == 'POST':
        ser.write('s'.encode("ASCII"))
        resultado = send_commands()
        if resultado is "ok":
            return render(request, 'copy/key_finish.html')
        else:
            error = True
            return render(request, 'copy/key_code.html', {'error3': error})

    return render(request, 'copy/key_cut.html')


@serial_connection_required
def key_payment(request):
    # What you want tha button to do.
    # email: mdiebr-buyer@gmail.com
    # pw: easykeyteste
    value = random.randint(1, 100)
    token = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(15))

    paypal_dict = {
        "business": "mdiebr-facilitator@gmail.com",
        "amount": "{}".format(value),
        "item_name": "Cópia de chave - Teste {}".format(value),
        "invoice": "{}".format(token),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('key_cut')),
        "cancel_return": request.build_absolute_uri(reverse('home')),
        "custom": "premium_plan",
        "currency_code": "BRL",
    }

    payment = Payment()

    payment.value = value
    payment.token = token
    payment.timestamp = datetime.datetime.now()

    payment.save()

    form = PayPalPaymentsForm(initial=paypal_dict)

    context = {"form": form}
    return render(request, "copy/key_payment.html", context)


def key_finish(request):
    return render(request, 'copy/key_finish.html')


def hello_msg():
    hour = datetime.datetime.now().strftime('%H');
    hour = int(hour)
    if hour >= 0 and hour <= 11:
        message = "Bom Dia!"
    elif hour >= 12 and hour <= 17:
        message = "Boa Tarde!"
    else:
        message = "Boa Noite!"

    return message


def try_to_connect():
    global ser
    for i in range(10):
        ser = serial_connection(i)
        if ser:
            break;


def serial_connection(value):
    try:
        ser = serial.Serial('/dev/ttyACM{}'.format(value), 9600,
                            timeout=None)
        return ser
    except:
        return 0


def send_commands():
    global ser
    resultado = 'a'
    file = open("media/gcode.nc")

    for line in file:
        time.sleep(1)
        ser.write((line[:-1]+'f').encode('ASCII'))
    
        while not resultado in ('c',):
            resultado = ser.read_all().decode('ASCII')
    if resultado == 'q':
        return "erro"
    resultado = 'a'
    return "ok"
