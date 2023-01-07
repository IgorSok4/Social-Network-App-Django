from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

# User. Model użykowanika wraz z podstawowymi kolumnami, takimi jak:
# - username
# - password
# - email
# - first_name
# - last_name
# - is_active

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])    # dane username i password zaciągnięte z LoginForm -> username, password z .forms.py
            if user is not None:
                if user.is_active:   # patrz wyżej na komentarz odnośnie modelu User. i jego kolumn
                    login(request, user)
                    return HttpResponse('Authentication was successful.')
                else:
                    return HttpResponse('The account is inactive.')
            else:
                return HttpResponse('Invalid credentials. Try again!')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {"section": 'dashboard'})