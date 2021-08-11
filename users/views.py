from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from draw.forms import ParticipantsForm
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
        currentUser = getCurrentUser(request)
        formset = formsetWithDataFromDB(currentUser)

        rowToDelete = ''
        if request.method == 'POST':
            if request.POST['delete']:
                rowToDelete = deleteRowFromDB(request, currentUser)
                messages.success(request, f'Participant {rowToDelete} has been successfully deleted from database.')
                formset = formsetWithDataFromDB(currentUser)         
    
    context = {
        'formset': formset,
        'rowToDelete': rowToDelete
    }
    return render (request, 'users/profile.html', context)

def getCurrentUser(request):
    userLoggedIn = request.user.username
    currentUser = User.objects.filter(username=userLoggedIn).first()
    return currentUser

def formsetWithDataFromDB(currentUser):
    ParticipantsFormset = inlineformset_factory(User, Participant, form=ParticipantsForm, extra=0)
    formset = ParticipantsFormset(instance=currentUser)
    return formset

def deleteRowFromDB(request, currentUser):
    rowNumber = int(request.POST['delete']) - 1
    email = request.POST[f'participant_set-{rowNumber}-email']
    rowToDelete = currentUser.participant_set.get(email=email)
    rowToDelete.delete()
    return rowToDelete