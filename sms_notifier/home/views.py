from django.shortcuts import render

def home(request):
	return render(request, 'home/home.html')

def settings(request):
	return render(request, 'home/settings.html')