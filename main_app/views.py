from distutils.log import error
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import SignUpForm
from.models import Profile


# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # request.method == 'GET'
    form = SignUpForm()
    context = {'form': form, 'error_message': error_message}            
    return render(request, 'registration/signup.html', context)


def home(request):
    return render(request, 'home.html')