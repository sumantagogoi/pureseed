from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.conf import settings
from .models import *


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.all().select_related('shippingaddress_set')

    context={'title': 'Manxho Dashboard', 'username': username, 'scale': "0.6", 'data': data}

    return render(request, 'list-orders.html', context)


def items(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Product.objects.all()

    context={'title': 'Manxho Dashboard', 'username': username, 'scale': "0.6",  'data': data}
    return render(request, 'list-items.html', context)


def cashReg(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = Order.objects.all()

    context={'title': 'Manxho Dashboard', 'username': username, 'scale': "0.6", 'msg': 'cash register'}

    return render(request, 'blank.html', context)


def customers(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    username = request.user.username

    data = User.objects.all()

    context={'title': 'Manxho Dashboard', 'username': username, 'scale': "0.6", 'data': data}

    return render(request, 'list-customers.html', context)