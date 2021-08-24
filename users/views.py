from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from draw.forms import ParticipantsForm
from draw.views import findRandomPairs, sendEmailToEveryParticipant, generateErrorIfSendingEmailFails, redirectToDrawingResultPage
from django.core.exceptions import ObjectDoesNotExist


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
        form = ParticipantsForm()
        group = ''
        
        if request.method == 'POST':

            if request.POST.get('deleteAddOrDraw') != '' and request.POST.get('deleteAddOrDraw') != 'add' and request.POST.get('deleteAddOrDraw') != 'draw':
                rowToDelete = deleteRowFromDB(request, currentUser)
                messages.success(request, f'Participant {rowToDelete} has been successfully deleted from database.')

            elif request.POST.get('deleteAddOrDraw') == 'add':
                name, email, form = getFormData(request, currentUser)

                if form.is_valid():
                    errorMessageName = doNotAcceptSameNames(request, currentUser, name)
                    errorMessageEmail = doNotAcceptSameEmails(request, currentUser, email)

                    if errorMessageName != True and errorMessageEmail != True:
                        form.save()
                        form = ParticipantsForm()
                           
            elif request.POST.get('deleteAddOrDraw') == 'draw':
                group = createDictWithDataFromDB(currentUser)
                pairs = findRandomPairs(group)
                
                """send emails"""
                errorMessagesFromSendingEmail = sendEmailToEveryParticipant(pairs, group)
                if True in errorMessagesFromSendingEmail:
                    generateErrorIfSendingEmailFails(request)
                else:
                    return redirectToDrawingResultPage(group, request) 


    context = {
        'form': form,
        'participants': participants
    }
    return render (request, 'users/profile.html', context)

def getCurrentUser(request):
    userLoggedIn = request.user.username
    currentUser = User.objects.filter(username=userLoggedIn).first()
    return currentUser

def deleteRowFromDB(request, currentUser):
    rowNumber = int(request.POST['deleteAddOrDraw']) - 1
    rowToDelete = currentUser.participant_set.all()[rowNumber]
    rowToDelete.delete()
    return rowToDelete

def getFormData(request, currentUser):
    name = request.POST['name']
    email = request.POST['email']
    form = ParticipantsForm({'name': name, 'email': email, 'user': currentUser})
    return name, email, form

def doNotAcceptSameNames(request, currentUser, name):
    try:
        if currentUser.participant_set.get(name=name):
            messages.error(request, 'Person with that name already exists')
            errorMessageName = True
            return errorMessageName
    except ObjectDoesNotExist:
        errorMessageName = False

def doNotAcceptSameEmails(request, currentUser, email):
    try:
        if currentUser.participant_set.get(email=email):
            messages.error(request, 'Person with that email already exists')
            errorMessageEmail = True
            return errorMessageEmail
    except ObjectDoesNotExist:
        errorMessageEmail = False

def createDictWithDataFromDB(currentUser):
    '''creating dictionary with participatns names and emails in following format:
    group['name'] = {'email': 'email@example.com'}'''
    group = {}
    for i in range(len(currentUser.participant_set.all())):
        group[currentUser.participant_set.all()[i].name] = {'email': currentUser.participant_set.all()[i].email}
    return group