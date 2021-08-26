from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.core.mail import send_mail
import random

def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)

    if request.method == 'POST':
        if request.POST['addSubtractOrDraw'] == 'add':
            formset = addRow(request, ParticipantsFormset)

        elif request.POST['addSubtractOrDraw'] == 'subtract':
            formset, error = subtractRow(request, ParticipantsFormset)
            
        elif request.POST['addSubtractOrDraw'] == 'draw':
            formset = ParticipantsFormset(request.POST)
            errorMessages = fullValidation(request, formset)

            # Displaying all errors
            for message in errorMessages:
                messages.error(request, message)
           
            if formset.is_valid() and errorMessages == []:
                group = createDictWithFormData(request)
                pairs = findRandomPairs(group)
                
                """send emails"""
                errorMessagesFromSendingEmail = sendEmailToEveryParticipant(pairs, group)
                if True in errorMessagesFromSendingEmail:
                    generateErrorIfSendingEmailFails(request)
                else:
                    return redirectToDrawingResultPage(group, request)                          
    else:
        #if no POST data - show empty form with 3 rows
        formset = generateEmptyForm(ParticipantsFormset)


    context = {
        'title': 'Home',
        'formset': formset
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
    error = messages.warning(request, 'There must be at least 3 participants.')
    return formset, error

def subtractRow(request, ParticipantsFormset):
    if int(request.POST['form-TOTAL_FORMS']) == 3: # At least 3 rows
        formset, error = warningAtLeast3Participants(request, ParticipantsFormset)
    else:
        formset, error = subtractRowSuccess(request, ParticipantsFormset)
    return formset, error

def checkForStandartFormsetErrors(formset):
    errorMsg = []
    for i in range(len(formset.errors)):
        for key in formset.errors[i]:
            if formset.errors[i][key]:
                errorMsg.append(formset.errors[i][key])
    return errorMsg

def translatingStandartFormsetErrorsToPolish(errorMsg):
    errorMessages = []
    if ['This field is required.'] in errorMsg:
        errorMessages.append('Fill out missing fields.')
    if ['Enter a valid email address.'] in errorMsg:
        errorMessages.append('Enter a valid email address.')
    return errorMessages

def finalFormsetErrors(formset):
    errorMsg = checkForStandartFormsetErrors(formset)
    errorMessages = translatingStandartFormsetErrorsToPolish(errorMsg)
    return errorMessages

def standardValidation(formset):
    if formset.is_valid():
        errorMessages = []
    else:
        if formset.errors:
            errorMessages = finalFormsetErrors(formset)
    return errorMessages

def doNotAcceptEmptyRows(request):
    errorMessages = []
    for i in range(int(request.POST['form-TOTAL_FORMS'])):
        if request.POST[f'form-{i}-name'] == '' and request.POST[f'form-{i}-email'] == '':
            text = 'Fill out missing rows.'
            if text not in errorMessages:
                errorMessages.append(text)
    return errorMessages

def doNotAcceptSameNames(request):
    errorMessages = []
    names = []
    for i in range(int(request.POST['form-TOTAL_FORMS'])):
        if request.POST[f'form-{i}-name'] == '':
            continue
        elif request.POST[f'form-{i}-name'] in names:
            text = 'Names cannot be repeated (If you have participants with the same names – use nicknames or surnames).'
            if text not in errorMessages:
                errorMessages.append(text)
        else:
            names.append(request.POST[f'form-{i}-name'])
    return errorMessages

def doNotAcceptSameEmailAddresses(request):
    errorMessages = []
    emails = []
    for i in range(int(request.POST['form-TOTAL_FORMS'])):
        if request.POST[f'form-{i}-email'] == '':
            continue
        if request.POST[f'form-{i}-email'] in emails:
            text = 'Emails cannot be repeated.'
            if text not in errorMessages:
                errorMessages.append(text)   
        else:
            emails.append(request.POST[f'form-{i}-email'])
    return errorMessages

def additionalValidation(request):
    errorMessages = []
    errorMessages += doNotAcceptEmptyRows(request)
    errorMessages += doNotAcceptSameNames(request)
    errorMessages += doNotAcceptSameEmailAddresses(request)
    return errorMessages

def fullValidation(request, formset):
    errorMessages = standardValidation(formset)
    errorMessages += additionalValidation(request)
    return errorMessages
                
def createListWithAllParticipantsNames(group):
    allNames = list(group.keys())
    return allNames

def randomPair(allNamesCopy):
    '''Finding random pair'''
    randomPersonIndex = random.randint(0, len(allNamesCopy) - 1)
    pair = allNamesCopy[randomPersonIndex]
    return pair, randomPersonIndex

def findPairForEveryParticipant(allNames):
    allNamesCopy = allNames[:]
    pairs = []        
    # for every person 
    for i in range(len(allNames)):
        # find pair
        pair, randomPersonIndex = randomPair(allNamesCopy)
        # you can not make a gift for yourself. If so, draw again:
        while allNames[i] == pair:
            pair, randomPersonIndex = randomPair(allNamesCopy)
        pairs.append((allNames[i], pair))
        allNamesCopy.pop(randomPersonIndex)
    return pairs

def findRandomPairs(group):
    allNames = createListWithAllParticipantsNames(group)
    pairs = findPairForEveryParticipant(allNames)
    return pairs

def prepareDataForSendingEmail(pairs, group, i):
    personWho = pairs[i][0]
    personWhom = pairs[i][1]
    sendTo = group[personWho]['email']
    title = 'Secret santa drawing'
    mailMessage = f'Hi {personWho}\nYou are taking part in a Secret Santa drawing. \nMake a gift for: {personWhom}.\nKind regards,\nSecret santa'
    return title, mailMessage, sendTo

def sendEmail(title, mailMessage, sendTo):
    try:
        send_mail(title, mailMessage, 'secretsanta.losowanie@gmail.com', [sendTo])
        errorMessageSendEmail = False
    except:
        errorMessageSendEmail = True
    return errorMessageSendEmail

def sendEmailToEveryParticipant(pairs, group):
    errorMessagesFromSendingEmail = []
    for i in range(len(pairs)):
        title, mailMessage, sendTo = prepareDataForSendingEmail(pairs, group, i)
        errorMessagesFromSendingEmail.append(sendEmail(title, mailMessage, sendTo))
    return errorMessagesFromSendingEmail

def generateErrorIfSendingEmailFails(request):
    messages.error(request, 'There has been a problem with sending email. Ty again later.')

def createDictWithFormData(request):
    '''creating dictionary with participatns names and emails in following format:
    group['name'] = {'email': 'email@example.com'}'''
    group = {}
    for i in range(int(request.POST['form-TOTAL_FORMS'])):
        group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']}
    return group

def redirectToDrawingResultPage(group, request):
    allParticipants = createDictWithAllParticipatsNamesAndEmails(group)
    request.session['participants'] = allParticipants
    return redirect('draw-drawing-result')

def drawingResult(request):
    return render(request, 'draw/drawing-result.html')