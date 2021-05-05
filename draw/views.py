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
                #creating dictionary "group" wi th participatns names and emails in following format:
                #group['name']: {'email': 'email@example.com'}
                for i in range(int(request.POST['form-TOTAL_FORMS'])):
                    #excluding empty rows:
                    if request.POST[f'form-{i}-name'] == '':
                        continue
                    else:
                        group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']}
                #creating list with all participtants names
                allNames = list(group.keys())
                #at least 3 participants:
                if len(allNames) < 3:
                    messages.warning(request, 'Liczba osób nie może być mniejsza niż 3.')
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
                messages.warning(request, 'Uzupełnij brakujące pola.')

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
    }
    return render(request, 'draw/home.html', context)





   