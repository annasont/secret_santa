from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    noOfRows = 3
    ParticipantsFormset = formset_factory(ParticipantsForm, extra=noOfRows)
    formset = ParticipantsFormset()

    valid = ''
    if request.method == 'POST':
        formset = ParticipantsFormset(request.POST)
        if formset.is_valid():
            valid = request.POST
    else:
        formset = ParticipantsFormset() 
 
    context = {
        'title': 'Home',
        'formset': formset,
        'valid': valid
    }
    return render(request, 'draw/home.html', context)





   