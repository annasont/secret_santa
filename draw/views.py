from django.shortcuts import render


def home(request):
    valueRowsButtonInRow = 4
    valueRowsButtonToggle = 4
    no = 3
    add = True
    substract = False


    if request.GET and request.GET['rows']:
        no = int(request.GET['rows'])
        valueRowsButtonInRow = no + 1
        valueRowsButtonToggle = no - 1
        add = True
        substract = False
    
    if request.POST and request.POST.get('minusRows'):
        no = int(request.GET['rows'])
        valueRowsButtonInRow = no - 1
        valueRowsButtonToggle = no + 1
        add = False
        substract = True
  
    context = {
        'title': 'Home',
        'no': no,
        'valueRowsButtonInRow': valueRowsButtonInRow,
        'valueRowsButtonToggle': valueRowsButtonToggle,
        'add': add,
        'subtract': substract
    }
    return render(request, 'draw/home.html', context)