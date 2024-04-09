from django.shortcuts import render, redirect
from .decorators import require_login
from ..models import *

@require_login
def feed(request):
   return render(request, 'user/feed.html', {'sess': request.session})

@require_login
def reuser(request):
   return redirect(user, username=request.session['username'])

@require_login
def user(request, username):
   pro = Profile.objects.get(username=username)
   if username == request.session['username']:
      isusr = True
   else:
      isusr = False
   return render(request, 'user/profile.html', {'pro': pro, 'res': 2, 'isusr': isusr, 'sess': request.session})