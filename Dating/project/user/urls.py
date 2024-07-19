from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('about', views.AboutView.as_view(), name='about'),
    path('signup', views.signup, name='signup'),
    # path('login', views.LoginView.as_view(), name='login'),
    path('matching', views.MatchingView.as_view(), name='matching'),
    path('test', views.TestView.as_view(), name='test'),
    path('test2', views.TestView2.as_view(), name='test2'),
    path('createprofile', views.CreateProfileView.as_view(), name='createprofile'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('plans', views.PlansView.as_view(), name='plans'),
    # path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    # path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login", views.signin, name="signin"),
    path('create_profile/', views.P_info_CreateView.as_view(), name='create_pinfo'),
    path('profile/update/<int:id>/', views.P_info_UpdateView.as_view(), name='profile_update'),
    path('Additional_info/', views.A_info_CreateView.as_view(), name='create_ainfo'),
    path('Additional_info/update/<int:id>/', views.A_info_UpdateView.as_view(), name='update_ainfo'),
    path('usermedia_create/', views.UserMediaCreateView.as_view(), name='create_media'),
    path('usermedia_update/<int:pk>/', views.UserMediaUpdateView.as_view(), name='update_media'),
    path('employeeinfo/',views.EmployeeinfoView.as_view(), name='emp_status'),
    path('matches/',views.Matches.as_view(), name='matches'),
    path('hide_profile/<int:user_id>/', views.hide_profile, name='hide_profile'),
    path('like/<int:user_id>/',views.like_profile, name='like_profile'),
    
    #friend 
    path('send_friend_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends_list/', views.friends_list, name='friends'),
    

]
