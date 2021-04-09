from django.shortcuts import render

# Create your views here.

def home(request):
    if request.GET and request.GET['rows']:
        no = int(request.GET['rows']) + 1
    else:
        no = 3
  
    context = {
        'title': 'Home',
        'no': no
    }
    return render(request, 'draw/home.html', context)