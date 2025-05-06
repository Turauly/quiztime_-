from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from .forms import RegisterForm

def logout_view(request):
    logout(request)
    return redirect('login')  # Шыққан соң логин бетіне қайта бағыттаймыз

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Тіркелген соң бірден логин
            return redirect('home')  # ✅ Негізгі бетке бағыттау
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
