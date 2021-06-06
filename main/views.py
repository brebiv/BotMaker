from django.shortcuts import render


def index(request):
    return render(request, 'main/lander.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')
