from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
# from draw.forms import ParticipantsForm
from draw.models import Participant

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}! Your account has been created. You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def loginUser(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in.')
                return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_authenticated:
        userLoggedIn = request.user.username
    
    currentUser = User.objects.filter(username=userLoggedIn).first()
    userParticipants = currentUser.participant_set.all()

    ParticipantsFormset = inlineformset_factory(User, Participant, fields=('name', 'email'), extra=3)
    formset = ParticipantsFormset()
    
    context = {
        'formset': formset,
        'userParticipants': userParticipants
    }
    return render (request, 'users/profile.html', context)