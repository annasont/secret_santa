from django.shortcuts import render

# Create your views here.

def home(request):
    if request.GET and request.GET['rows']:
        no = int(request.GET['rows'])
    else:
        no = 3
  
    context = {
        'title': 'Home',
        'no': no,
        'valueRowsButton': no + 1
    }
    return render(request, 'draw/home.html', context)