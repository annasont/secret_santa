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
    x = []
    errorMessage = ''

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
                x = formset.cleaned_data
                #creating dictionary "group" with participatns names and emails in following format:
                #group['name']: {'email': 'email@example.com'}
                for i in range(int(request.POST['form-TOTAL_FORMS'])):
                    if request.POST[f'form-{i}-name'] == '':
                        continue
                    else:
                        group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']}
                #creating list with all participtants names
                allNames = list(group.keys())
                #no empty rows:
                if len(allNames) != int(request.POST['form-TOTAL_FORMS']):
                    errorMessage = 'Uzupełnij brakujące rzędy w formularzu.'
                else:
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
                        errorMessage = 'Uzupełnij brakujące pola.'
                    elif errorMessage == ['Enter a valid email address.']:
                        errorMessage = 'Wprowadź poprawne adresy email.'

            messages.error(request, errorMessage)

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
        'x': x
    }
    return render(request, 'draw/home.html', context)





   