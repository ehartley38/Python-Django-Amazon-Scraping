from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    #If we get a post request, the it instantiates a form with the POST data.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login')
            return redirect('login')
    #If not post request (e.g. GET request), then a blank form is created
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required #Require user is logged in before they can view profile
def profile(request):
    return render(request, 'users/profile.html')




'''
messages.debug
messages.info
messages.success
messages.warning
messages.error
'''