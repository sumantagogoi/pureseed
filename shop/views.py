from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth.models import User

from django.conf import settings
from .models import *
from .forms import PinCodeForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.filter(Q(status="order_confirmed") | Q(status="dispatched") | Q(status="processing")).select_related('shippingaddress')

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data, 'status': "Confirmed"}

    return render(request, 'list-orders.html', context)


def items(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Product.objects.all()

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6",  'data': data}
    return render(request, 'list-items.html', context)


def cashReg(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.all()

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'msg': 'cash register'}

    return render(request, 'blank.html', context)


def customers(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = User.objects.all()

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data}

    return render(request, 'list-customers.html', context)


def confirmUPI(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.filter(status="upi_unconfirmed").select_related('shippingaddress')

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data}

    return render(request, 'list-upi.html', context)


def cancelledOrders(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.filter(status="cancelled").select_related('shippingaddress')

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data, 'status': "Cancelled"}

    return render(request, 'list-orders.html', context)

def completedOrders(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.filter(status="completed").select_related('shippingaddress')

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data, 'status': "Completed"}

    return render(request, 'list-orders.html', context)

def editPin(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = PinCode.objects.all()

    if request.method == "POST":
        form = PinCodeForm(request.POST)
        
        if form.is_valid():
            form.save()
        else:
            if PinCode.objects.filter(pincode=request.POST.get("pincode")).exists():
                obj = PinCode.objects.get(pincode=request.POST.get("pincode"))
                obj.servicibility = form.cleaned_data["servicibility"]
                obj.place = form.cleaned_data["place"]
                obj.state = form.cleaned_data["state"]
                obj.notes = form.cleaned_data["notes"]
                obj.save() 

    form = PinCodeForm()

    context={'title': 'Pureseed Dashboard', 'username': username, 'scale': "0.6", 'data': data, 'form': form}

    return render(request, 'list-pin.html', context)