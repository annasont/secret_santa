from django.shortcuts import render
from django.contrib import messages
from .forms import ParticipantsForm


def home(request):
    form = ParticipantsForm(request.POST or None)
    
    valueRowsButtonInRow = 4
    valueRowsButtonToggle = 2
    no = 3
    # add = True
    # substract = False
    # message = ''

    # if request.GET and request.GET['rows']:
    #     if int(request.GET['rows']) < 3:
    #         messages.warning(request, 'Liczba osób nie może być mniejsza niż 3')
    #         no = 3
    #     else:
    #         no = int(request.GET['rows'])
    #     valueRowsButtonInRow = no + 1
    #     valueRowsButtonToggle = no - 1
    #     add = True
    #     substract = False
    
    # if request.POST and request.POST.get('minusRows'):
    #     if int(request.GET['rows']) < 3:
    #         message = 'no can do'
    #         no = 3
    #     else:
    #         no = int(request.GET['rows'])
    #     valueRowsButtonInRow = no - 1
    #     valueRowsButtonToggle = no + 1
    #     add = False
    #     substract = True

    # #testowanie
    # x = ''
    # if request.POST:
    #     x = request.POST
    # #koniec
  
    context = {
        'title': 'Home',
        'form': form,
        'no': no,
        'valueRowsButtonInRow': valueRowsButtonInRow,
        'valueRowsButtonToggle': valueRowsButtonToggle,
        # 'add': add,
        # 'subtract': substract,
        # 'message': message,
        # 'x': x
    }
    return render(request, 'draw/home.html', context)