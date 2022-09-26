from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import string
import random

from .forms import UserCreateForm, UserAuthenticationForm
from .notification_manager import send_email
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserAuthenticationForm()
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            return redirect('index')

    return render(request, 'login.html', context={"form": form})


def login_view_admin(request):
    user = User.objects.get(pk=1)
    login(request, user)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            send_email(7, [new_user], from_user=None)
            return redirect('select_locations')
    return render(request, 'register.html', context={"form": form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('index')


# NOT USED ANYMORE
def generate_user_temp_password_key():
    uid_key_generated = [random.choice(string.ascii_letters + string.digits) for i in range(50)]
    uid_key = "".join(uid_key_generated)
    return uid_key
