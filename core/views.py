from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from pprint import pprint
User = get_user_model()


def LogInView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('rooms:home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User %s does not exist' % username)
            return redirect('core:login')

        if check_password(password, user.password):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('rooms:home')
            messages.error(request, 'Authentication fialed')
        
        messages.error(request, 'Invalid password')

    return render(request, 'core/login_register.html', {'page':page})



def LogOutView(request):
    logout(request)
    return redirect('rooms:home')


def RegisterView(request):
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        pprint(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('rooms:home')
            messages.error(request, 'Authenication failed')
        messages.error(request, 'Form validation failed')
    
    else:
        form = UserCreationForm()


    context = {'form':form, 'page':page}

    return render(request, 'core/login_register.html', context)