from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name='logout'),
    path('leaderboard/', views.leaderboard_view, name="leaderboard"),
    path('fraud/', views.fraud, name='fraud'),
    path('submit_exam/', views.submit_exam, name='submit_exam'),
]