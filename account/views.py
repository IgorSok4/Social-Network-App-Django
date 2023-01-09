from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# User. Model użykowanika wraz z podstawowymi kolumnami, takimi jak:
# - username
# - password
# - email
# - first_name
# - last_name
# - is_active

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Utworzenie nowego obiektu użytkownika; jednak jeszcze nie zapiosujemy go w bazie danych
            new_user = user_form.save(commit=False)
            #Ustawienie wybranego hasła
            new_user.set_password(user_form.cleaned_data['password'])
            #Zapisanie obiektu user
            new_user.save()
            #Utworzenie profilu użytkownika
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form})
    
    
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
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
