from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomLoginForm()

    return render(request, 'user/login.html', {"form": form})


def signout(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('home')
        else:
            messages.error(request, "Invalid user details")

    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {"form": form})
