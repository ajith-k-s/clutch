from django.shortcuts import render, redirect
from .decorators import require_login
from ..models import *

@require_login
def settings(request):
   return redirect(account)

@require_login
def account(request):
   usr = Profile.objects.get(id = request.session['uid'])
   if request.method == 'POST':
      if request.POST['action'] == 'save':
         if request.POST['username'] != usr.username:
            usr.username = request.POST['username']
         if request.POST['name'] != usr.name:
            usr.name = request.POST['name']
         if request.POST['bio'] != usr.bio:
            usr.bio = request.POST['bio']
         try:
            usr.save()
            request.session['username'] = usr.username
            err = '0'
         except:
            err = '1'
         usr = Profile.objects.get(id = request.session['uid'])
         return render(request, 'settings/account.html', {'usr': usr, 'err': err, 'sess': request.session})
      elif request.POST['action'] == 'cancel':
         return render(request, 'settings/account.html', {'usr': usr, 'sess': request.session})
   else:
      return render(request, 'settings/account.html', {'usr': usr, 'sess': request.session})
   
@require_login
def theme(request):
   return render(request, 'settings/themeselector.html', {'sess': request.session})