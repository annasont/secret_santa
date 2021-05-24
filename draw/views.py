from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.core.mail import send_mail
import random, smtplib, os


def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)
    
    errorMessages = []
    pairs = []

    if request.method == 'POST':
        # Adding new row (button "+ Dodaj kolejną osobę" pressed)
        if request.POST['addSubtractOrDraw'] == 'add':
            formset = addRow(request, ParticipantsFormset)

        # Deliting last row (button "- Usuń ostatni rząd pressed")
        elif request.POST['addSubtractOrDraw'] == 'subtract':
            formset, error = subtractRow(request, ParticipantsFormset)
            
        # Drawing (button "Losuj" pressed)
        elif request.POST['addSubtractOrDraw'] == 'draw':
            formset = ParticipantsFormset(request.POST)
            
            # Standard validation
            if formset.is_valid():
                pass
            else:
                errorMsg = []
                if formset.errors:
                    for i in range(len(formset.errors)):
                        for key in formset.errors[i]:
                            if formset.errors[i][key]:
                                errorMsg.append(formset.errors[i][key])

                    if ['This field is required.'] in errorMsg:
                        errorMessages.append('Uzupełnij brakujące pola.')
                    if ['Enter a valid email address.'] in errorMsg:
                        errorMessages.append('Niepoprawny adres email.')

            # Additional validation.
            names = []
            emails = []
            for i in range(int(request.POST['form-TOTAL_FORMS'])):
                # Can not accept empty rows:
                if request.POST[f'form-{i}-name'] == '' and request.POST[f'form-{i}-email'] == '':
                    text = 'Uzupełnij brakujące rzędy.'
                    if text not in errorMessages:
                        errorMessages.append(text)
                
                # Can not accept same names:
                if request.POST[f'form-{i}-name'] in names:
                    text = 'Imiona nie mogą się powtarzać (jeżeli w losowaniu biorą udział osoby o tych samych imionach, wpisz ksywy / nazwiska / coś co pozwoli zidentyfikować właściwą osobę).'
                    if text not in errorMessages:
                        errorMessages.append(text)
                else:
                    names.append(request.POST[f'form-{i}-name'])

                # Can not accept same email addresses:
                if request.POST[f'form-{i}-email'] in emails:
                    text = 'Adresy email nie mogą się powtarzać.'
                    if text not in errorMessages:
                        errorMessages.append(text)   
                else:
                    emails.append(request.POST[f'form-{i}-email'])

            # Displaying all errors
            for message in errorMessages:
                messages.error(request, message)

            # If formset is valid
            group = {}       
            if formset.is_valid() and errorMessages == []:
                # And creating dictionary "group" with participatns names and emails in following format:
                # group['name'] = {'email': 'email@example.com'}
                for i in range(int(request.POST['form-TOTAL_FORMS'])):
                    group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']}
                
                # creating list with all participtants names
                allNames = list(group.keys())
                allNamesCopy = allNames[:]
                

                # for every person 
                for i in range(len(allNames)):
                    # find pair
                    pair, randomPersonIndex = randomPair(allNames, allNamesCopy)
                    # you can not make a gift for yourself. If so, draw again:
                    while allNames[i] == pair:
                        pair, randomPersonIndex = randomPair(allNames, allNamesCopy)
                    pairs.append((allNames[i], pair))
                    allNamesCopy.pop(randomPersonIndex)
                
                """send emails"""
                message = False
                for i in range(len(pairs)):
                    personWho = pairs[i][0]
                    personWhom = pairs[i][1]
                    sendTo = group[personWho]['email']
                    title = 'Losowanie secret santa'
                    mailMessage = f'Cześć {personWho}\nBierzesz udział w losownaniu secret santa.\nOsoba, której robisz prezent to: {personWhom}.\nPozdrawiam,\nSecret santa'
                    # try:
                    #     send_mail(title, mailMessage, 'secretsanta.losowanie@gmail.com', [sendTo])
                    # except:
                    #     message = True
                    
                if message == True:
                    messages.error(request, 'Wystąpił problem z wysłaniem maili. Spróbuj ponownie później.')
                if message == False:
                    allParticipants = createDictWithAllParticipatsNamesAndEmails(group)
                    request.session['participants'] = allParticipants
                    return redirect('draw-drawing-result')             
                
    else:
        #if no POST data - show empty form with 3 rows
        formset = generateEmptyForm(ParticipantsFormset)


    context = {
        'title': 'Home',
        'formset': formset,
        'pairs': pairs,
    }
    return render(request, 'draw/home.html', context)


def createDictWithAllParticipatsNamesAndEmails(group):
    participants = []
    for person in group:
        participants.append(f"{person} ({group[person]['email']})")
    return participants

def generateEmptyForm(ParticipantsFormset):
    noOfRows = 3
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
    formset = ParticipantsFormset()
    return formset

def addRow(request, ParticipantsFormset):
    requestPostData = request.POST.copy()
    requestPostData['form-TOTAL_FORMS'] = int(requestPostData['form-TOTAL_FORMS']) + 1
    formset = ParticipantsFormset(requestPostData)
    return formset

def subtractRowSuccess(request, ParticipantsFormset):
    requestPostData = request.POST.copy()
    requestPostData['form-TOTAL_FORMS'] = int(requestPostData['form-TOTAL_FORMS']) - 1
    formset = ParticipantsFormset(requestPostData)
    error = ''
    return formset, error

def warningAtLeast3Participants(request, ParticipantsFormset):
    requestPostData = request.POST.copy()
    formset = ParticipantsFormset(requestPostData)
    error = messages.warning(request, 'Liczba osób nie może być mniejsza niż 3.')
    return formset, error

def subtractRow(request, ParticipantsFormset):
    if int(request.POST['form-TOTAL_FORMS']) == 3: # At least 3 rows
        formset, error = warningAtLeast3Participants(request, ParticipantsFormset)
    else:
        formset, error = subtractRowSuccess(request, ParticipantsFormset)
    return formset, error

def randomPair(allNames, allNamesCopy):
    '''Finding random pair'''
    randomPersonIndex = random.randint(0, len(allNamesCopy) - 1)
    pair = allNamesCopy[randomPersonIndex]
    return pair, randomPersonIndex


def drawingResult(request):
    return render(request, 'draw/drawing-result.html')