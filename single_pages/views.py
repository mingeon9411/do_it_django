from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def landing(request):
    return render(request, 'single_pages/landing.html')

def about_me(request):
    return render(request, 'single_pages/about_me.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/blog/')
    else:
        form = UserCreationForm()
    return render(request, 'single_pages/signup.html', {'form': form})
