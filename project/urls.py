"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
   https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
handler404 = "core.views.page_not_found"

urlpatterns = [
   re_path(r'^favicon\.ico$', favicon_view),



   ###########################
   ###         Base        ###
   path("", views.index, name="index"),
   path("signin/", views.signin, name="signin"),
   path("signup/", views.signup, name="signup"),
   path("signout/", views.signout, name="signout"),
   ###         Base        ###
   ###########################



   ###########################
   ###         JSON        ###
   path("check-usr/", views.checkUsr, name="checkUsr"),
   path("check-like/", views.checkLike, name="checkLike"),
   path("toggle-like/", views.toggleLike, name="toggleLik"),
   path("toggle-follow/", views.toggleFollow, name="toggleFollow"),
   path("check-follow/", views.checkFollow, name="checkFollow"),
   ###         JSON        ###
   ###########################
   
   

   ###########################    
   ###      User page      ###
   path("feed/", views.feed, name="feed"),
   path("u/<str:username>/", views.user, name="user"),
   path("u/", views.reuser, name="reuser"),
   path("addpost/", views.addPost, name="addpost"),
   path("search/", views.search, name="search"),
   path("chat/", views.chatView, name="chatView-def"),
   path("chat/<str:username>/", views.chatView, name="chatView"),
   path("followers/", views.followers, name="followers"),
   path("followings/", views.followings, name="followings"),
   ###      User page      ###
   ###########################



   ###########################
   ###       Settings      ###
   path("settings/", views.settings, name="settings"),
   path("settings/account/", views.account, name="account"),
   path("settings/sign-in/", views.changePassword, name="changePassword"),
   ###       Settings      ###
   ###########################



   ###########################    
   ###      Admin page     ###
   path("userlist/", views.userlist, name="userlist"),
   path("editusr/<str:id>/", views.editusr, name="editusr"),
   path("blockusr/<int:id>/", views.blockusr, name="blockusr"),
   ###      Admin page     ###
   ###########################



   ###########################
   ###         Test        ###
   path('test/', views.test, name='test'),
   path('adder/', views.adder, name='adder'),
   path('theme/', views.theme, name='theme'),
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
