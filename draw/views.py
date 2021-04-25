from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    extra = 3

    valid = ''
    x = ''

    if request.method == 'POST':
        if request.POST['changeNoOfRows'] == 'add':
            extra = int(float(request.POST['extra'])) + 1
            # form = ParticipantsForm(initial=request.POST)
            ParticipantsFormset = formset_factory(ParticipantsForm, extra=extra)
            formset = ParticipantsFormset(request.POST)
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





   