from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, ProfileManager
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.exceptions import *
from .forms import UserForm, UserProfileInfoForm
from django.urls import reverse
# from django.shortcuts import render, redirect, get_object_or_404



# def index(request): 
#     return render(request, "home/mainpage.html", {})

def signup_view(request):
    registered = False
    if request.method=='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar=request.FILES['avatar']
            profile.save()

            registered = True

            return HttpResponseRedirect('/login')
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'home/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def login_view(request):
    # valuenext= request.POST.get()
    # print(valuenext )
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:

        return render(request, 'home/login.html', {})



# Create your views here.
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user
    context = {
        'profile': profile,
    }

    return render(request, 'home/myprofile.html', context)

# def like_unlike(request):
#     if request.method == 'POST':
#         account_id = request.POST.get('account_id')
#         profile_obj = Profile.objects.get(id=account_id)
#         profile_obj.liked.add("Like")

def profiles_list(request):
    profiles =Profile.objects.get_all_profiles()
    context = {
        'profiles': profiles,
    }

    return render(request, 'home/profiles_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model= Profile
    template_name = 'home/detail.html'

    # def get_object(self, slug=None):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile
    #     try: 
    #         profile = Profile.objects.get(slug=slug)
    #         return profile
    #     except:
    #         print('Data Not Found')
    #     finally: 
    #         return profile
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        try:
            user = User.objects.get(username__iexact=self.request.user) 
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            print('Data Not Found')
       
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'home/mainpage.html'
    #context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        try: 
            user = User.objects.get(username__iexact=self.request.user)
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            print('Data Not Found')
        
        return context