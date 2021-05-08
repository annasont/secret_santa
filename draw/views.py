from django.contrib.messages.api import error
from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError
import random


def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)

    message = ''
    group = {}
    pairs = []
    errorMessages = []
    allEmails = []
    x = []
    y = []

    if request.method == 'POST':
        # Adding new row
        if request.POST['addSubtractOrDraw'] == 'add':
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            formset = ParticipantsFormset(cp)
        # Deliting last row
        elif request.POST['addSubtractOrDraw'] == 'subtract':        
            if int(request.POST['form-TOTAL_FORMS']) == 3: # At least 3 rows
                cp = request.POST.copy()
                formset = ParticipantsFormset(cp)
                messages.warning(request, 'Liczba osób nie może być mniejsza niż 3.')
            else:
                cp = request.POST.copy()
                cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) - 1
                formset = ParticipantsFormset(cp)
        # Drawing
        elif request.POST['addSubtractOrDraw'] == 'draw':
            formset = ParticipantsFormset(request.POST)
            if formset.is_valid():
                # creating dictionary "group" with participatns names and emails in following format:
                # group['name']: {'email': 'email@example.com'}
                for i in range(int(request.POST['form-TOTAL_FORMS'])):
                    if request.POST[f'form-{i}-name'] == '':
                        continue
                    elif request.POST[f'form-{i}-email'] in allEmails:
                        errorMessages.append('Adresy email nie mogą się powtarzać')
                        group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']} 
                    else:
                        allEmails.append(request.POST[f'form-{i}-email'])
                        group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']} 
                        
                # creating list with all participtants names
                allNames = list(group.keys())
                # no empty rows:
                if len(allNames) != int(request.POST['form-TOTAL_FORMS']):
                    errorMessages.append('Uzupełnij brakujące rzędy.')
                
                if errorMessages == []:
                    allNamesCopy = allNames[:]
                    def randomPair(allNames, allNamesCopy):
                        # Finding random pair
                        randomPersonIndex = random.randint(0, len(allNamesCopy) - 1)
                        pair = allNamesCopy[randomPersonIndex]
                        return pair, randomPersonIndex
                    # for every person 
                    for i in range(len(allNames)):
                        # find pair
                        pair, randomPersonIndex = randomPair(allNames, allNamesCopy)
                        # you can not make a presenf for yourself. If so, draw again:
                        while allNames[i] == pair:
                            pair, randomPersonIndex = randomPair(allNames, allNamesCopy)
                        pairs.append((allNames[i], pair))
                        allNamesCopy.pop(randomPersonIndex)
            else:
                if formset.errors:
                    for i in range(len(formset.errors)):
                        for key in formset.errors[i]:
                            if formset.errors[i][key]:
                                errorMessage = formset.errors[i][key]

                    if errorMessage == ['This field is required.']:
                        errorMessages.append('Uzupełnij brakujące pola.')
                    elif errorMessage == ['Enter a valid email address.']:
                        errorMessages.append('Niepoprawny adres email.')

            for message in errorMessages:
                messages.error(request, message)
           


    else:
        #if no POST data show empty form with 3 rows
        noOfRows = 3
        ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
        formset = ParticipantsFormset() 


    context = {
        'title': 'Home',
        'formset': formset,
        'message': message,
        'pairs': pairs,
        'x': x,
        'y': y
    }
    return render(request, 'draw/home.html', context)





   #cleaned data