from django.urls import path
#from user import views as user_view 

from . import views

app_name = 'home'
urlpatterns = [
    #path('', views.index, name = 'mainpage'),
    path('', views.ProfileListView.as_view(), name = 'all-profiles-view'),
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', views.login_view, name = 'login'),
    path('myprofile/', views.my_profile_view, name = 'my-profile'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
]