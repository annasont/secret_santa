from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from draw.forms import ParticipantsForm
from draw.models import Participant
from draw.views import addRow

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
        participants = currentUser.participant_set.all()
        newParticipants = False
        ParticipantsFormset = inlineformset_factory(User, Participant, form=ParticipantsForm, extra=1)
        formset = ParticipantsFormset()
        test = ''
        

        rowToDelete = ''
        if request.method == 'POST':
            test = request.POST.get('deleteAddSubtractSaveOrDraw')

            if request.POST.get('deleteAddSubtractSaveOrDraw') != '' and request.POST.get('deleteAddSubtractSaveOrDraw') != 'add' and request.POST.get('deleteAddSubtractSaveOrDraw') != 'subtract' and request.POST.get('deleteAddSubtractSaveOrDraw') != 'draw':
                rowToDelete = deleteRowFromDB(request, currentUser)
                messages.success(request, f'Participant {rowToDelete} has been successfully deleted from database.')

            elif request.POST.get('deleteAddSubtractSaveOrDraw') == 'add':
                newParticipants = True
            #     formset = addRow(request, ParticipantsFormset)

            # elif request.POST['addSubtractOrDraw'] == 'subtract':
            #     formset, error = subtractRow(request, ParticipantsFormset)
            
            # elif request.POST['addSubtractOrDraw'] == 'draw':
            #     formset = ParticipantsFormset(request.POST)
            #     errorMessages = fullValidation(request, formset)

    context = {
        'formset': formset,
        'rowToDelete': rowToDelete,
        'participants': participants,
        'newParticipants': newParticipants,
        'test': test
    }
    return render (request, 'users/profile.html', context)

def getCurrentUser(request):
    userLoggedIn = request.user.username
    currentUser = User.objects.filter(username=userLoggedIn).first()
    return currentUser

# def formsetWithDataFromDB(currentUser):
#     ParticipantsFormset = inlineformset_factory(User, Participant, form=ParticipantsForm, extra=1)
#     formset = ParticipantsFormset(instance=currentUser)
#     return formset

# def deleteRowFromDB(request, currentUser):
#     rowNumber = int(request.POST['delete']) - 1
#     email = request.POST[f'participant_set-{rowNumber}-email']
#     rowToDelete = currentUser.participant_set.get(email=email)
#     rowToDelete.delete()
#     return rowToDelete

def deleteRowFromDB(request, currentUser):
    rowNumber = int(request.POST['deleteAddSubtractSaveOrDraw']) - 1
    rowToDelete = currentUser.participant_set.all()[rowNumber]
    rowToDelete.delete()
    return rowToDelete