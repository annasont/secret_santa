from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'title': 'Home',
        'no': [0, 1, 2]
    }
    return render(request, 'draw/home.html', {'title': 'Home'})