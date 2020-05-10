"""familjSpel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('startGame/', views.startGame, name="startGame"),
    path('', views.getHomePage, name="home"),
    path('user/', views.chooseUsername, name="user"),
    path('gamePage/', views.getGamePage, name="gamePage"),
    path('logout/', views.logout_view, name="logout"),
    path('startRound/', views.startRound, name="startRound"),
    path('postQuestion/', views.postQuestion, name="postQuestion"),
    path('postAnswer/', views.postAnswer, name="postAnswer"),
    path("getQuestion/", views.getQuestion, name="getQuestion"),  
    path("votables/", views.votables, name="votables"),
    path("votingPage/", views.votingPage, name="votingPage"),
    path("winningPage/", views.winningPage, name="winningPage"),
    path("resetRound/", views.resetRound, name="resetRound"),
    path("getWinner/", views.getWinner, name="getWinner"),
]
