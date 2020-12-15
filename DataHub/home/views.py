from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, ProfileManager
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.exceptions import *
# from django.shortcuts import render, redirect, get_object_or_404



# def index(request): 
#     return render(request, "home/mainpage.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("http://dailysensors.com/")
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})


def login_view(request):
    print(request.method)
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password) 
        if user is not None: 
            form = login(request, user)
            return HttpResponseRedirect("http://dailysensors.com/")
        else: 
            messages.info(request, 'Account does not exist. Please try again')
    form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})



# Create your views here.

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

class ProfileDetailView(DetailView):
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
        finally:
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
        finally:
            return context