from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=3)

    valid = ''
    x = ''

    if request.method == 'POST':
        if request.POST['changeNoOfRows'] == 'add':
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            formset = ParticipantsFormset(cp)
        elif request.POST['changeNoOfRows'] == 'subtract':
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) - 1
            formset = ParticipantsFormset(cp)


        if formset.is_valid():
            valid = request.POST

    else:
        noOfRows = 3
        ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
        formset = ParticipantsFormset() 
 
    

    context = {
        'title': 'Home',
        'formset': formset,
        'valid': valid,
        'x': x
    }
    return render(request, 'draw/home.html', context)





   