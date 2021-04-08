from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'title': 'Home',
        'no': 3
    }
    return render(request, 'draw/home.html', context)