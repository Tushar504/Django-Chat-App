from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def register(request):

    if request.method == "POST":
        data = request.POST

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/api/auth/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username)

        user.set_password(password)
        user.save()

        messages.info(request, "User Registerd")
        return redirect("/api/auth/login")

    return render(request, "register.html")


def login_page(request):

    if request.user.is_authenticated:
        return redirect("/api/auth/home")

    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if not user.exists():
            messages.info(request, "Invalid Username")
            return redirect("/api/auth/login")

        user = authenticate(username=username, password=password)

        if not user:
            messages.info(request, "Invalid Password")
            return redirect("/api/auth/login")
        else:
            login(request, user=user)
            next = request.GET.get("next")
            if next:
                return redirect(next)
            return redirect("/api/auth/home")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/api/auth/login")


def home(request):
    return render(request, "home.html")