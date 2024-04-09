from django.shortcuts import render, redirect
from ..models import *
from .decorators import require_admin, require_login

@require_login
@require_admin
def userlist(request):
   usrs=Profile.objects.all()
   return render(request,'admin/userlist.html',{'usrs':usrs, 'sess': request.session})

@require_login
@require_admin
def editusr(request, id):
   login = Profile.objects.get(id=id)
   return render(request,'admin/editusr.html', {'login':login, 'sess': request.session})

@require_login
@require_admin
def blockusr(request, username):
   login = Profile.objects.get(username=username)
   login.delete()
   return redirect(userlist)