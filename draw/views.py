from django.contrib.messages.api import error
from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
import random


def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)
    
    errorMessages = []
    pairs = []

    if request.method == 'POST':
        # Adding new row (button "+ Dodaj kolejną osobę" pressed)
        if request.POST['addSubtractOrDraw'] == 'add':
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            formset = ParticipantsFormset(cp)

        # Deliting last row (button "- Usuń ostatni rząd pressed")
        elif request.POST['addSubtractOrDraw'] == 'subtract':        
            if int(request.POST['form-TOTAL_FORMS']) == 3: # At least 3 rows
                cp = request.POST.copy()
                formset = ParticipantsFormset(cp)
                messages.warning(request, 'Liczba osób nie może być mniejsza niż 3.')
            else:
                cp = request.POST.copy()
                cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) - 1
                formset = ParticipantsFormset(cp)

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
                
                def randomPair(allNames, allNamesCopy):
                    '''Finding random pair'''
                    randomPersonIndex = random.randint(0, len(allNamesCopy) - 1)
                    pair = allNamesCopy[randomPersonIndex]
                    return pair, randomPersonIndex

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
                # Log to email account
                # Send emails
                # Redirect to page with success message
                
    else:
        #if no POST data show empty form with 3 rows
        noOfRows = 3
        ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
        formset = ParticipantsFormset() 


    context = {
        'title': 'Home',
        'formset': formset,
        'pairs': pairs,
    }
    return render(request, 'draw/home.html', context)

def drawingResult(request):
    x = 'test'
    context = {
        'x': x
    }

    return render(request, 'draw/drawing-result.html', context)