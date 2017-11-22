from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
import datetime
import random
import string
import serial

from .models import Key, Payment

SERIAL = 0

def home(request):
    global SERIAL
    hour = datetime.datetime.now().strftime('%H');
    hour = int(hour)
    message = hello_msg(hour)

    if request.method == 'GET':
        for i in range(10):
            SERIAL = serial_connection(i)
            if SERIAL:
                break;
        if not SERIAL:
            error = True
            return render(request, 'copy/home.html', {'message': message,
                                                      'serial_error': error})
        return render(request, 'copy/home.html', {'message': message})
    if request.method == 'POST':
        if SERIAL:
            return redirect('key_code')
        else:
            error = True
            return render(request, 'copy/home.html', {'message': message,
                                                      'serial_error': error})


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
    if request.method == 'POST':
        send_commands(request)

    return render(request, 'copy/key_cut.html')


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


def hello_msg(hour):
    if hour >= 0 and hour <= 11:
        message = "Bom Dia!"
    elif hour >= 12 and hour <= 17:
        message = "Boa Tarde!"
    else:
        message = "Boa Noite!"

    return message


def serial_connection(value):
    try:
        ser = serial.Serial('/dev/ttyACM{}'.format(value), 9600,
                            timeout=None)
        return ser
    except:
        return 0


def send_commands(request):
    global SERIAL
    








CRIAR THREAD NESSA MERDA














    SERIAL.write('0'.encode('ASCII'))
    time.sleep(1)
    SERIAL.read_all()
    SERIAL.write('g0'.encode('ASCII'))

    # f = open("gcode.nc")
    # for l in f:
    # print(l.strip())
    # ser.write((l.strip() + "\n").encode("ASCII"))
    # ser.read(1)

