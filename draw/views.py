from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)

    message = ''
    valid = ''
    x = ''

    if request.method == 'POST':
        if request.POST['changeNoOfRows'] == 'add':
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            formset = ParticipantsFormset(cp)
        elif request.POST['changeNoOfRows'] == 'subtract':        
            if int(request.POST['form-TOTAL_FORMS']) == 3:
                cp = request.POST.copy()
                formset = ParticipantsFormset(cp)
                messages.warning(request, 'Liczba osób nie może być mniejsza niż 3.')
            else:
                cp = request.POST.copy()
                cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) - 1
                formset = ParticipantsFormset(cp)

        if formset.is_valid():
            valid = request.POST

    else:
        noOfRows = 3
        ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
        formset = ParticipantsFormset() 


    group = {}
    if request.method == 'POST':
        for i in range(int(request.POST['form-TOTAL_FORMS'])):
            group[request.POST[f'form-{i}-name']] = {'email': request.POST[f'form-{i}-email']}


    context = {
        'title': 'Home',
        'formset': formset,
        'message': message,
        'valid': valid,
        'group': group
    }
    return render(request, 'draw/home.html', context)





   