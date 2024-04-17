import os
from django.conf import settings
from django.shortcuts import render, redirect
from .decorators import require_login
from ..models import *

def delUsrImage(profile):
   if profile.image.name != 'blank_user.png':
      # Get the path of the previous image
      previous_image_path = os.path.join(settings.MEDIA_ROOT, profile.image.name)
      # Check if the file exists and delete it
      if os.path.exists(previous_image_path):
         os.remove(previous_image_path)


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
      elif request.POST['action'] == 'image':
         usr = Profile.objects.get(id=request.session['uid'])
         delUsrImage(usr)
         usr.image = request.FILES['usrpic']
         try:
            usr.save()
            request.session['profile_image'] = usr.image.url
            err = '0'
         except:
            err = '1'
         return render(request, 'settings/account.html', {'usr': usr, 'err': err, 'sess': request.session})
   else:
      return render(request, 'settings/account.html', {'usr': usr, 'sess': request.session})

@require_login
def changePassword(request):
   usr = Profile.objects.get(id = request.session['uid'])
   if request.method == "POST":
      if not check_password(usr.password, request.POST['passwd']):
         return render(request, 'passwd.html',{'err': "Incorrect Password"})
      passwd = make_password(request.POST['pass'])
      cpasswd = make_password(request.POST['cpass'])
      if passwd == cpasswd:
         usr.password = passwd
         try:
            usr.save()
            return render(request, 'passwd.html',{'scc': "Password Successfully Changed"})
         except:
            return render(request, 'passwd.html',{'err': "Failed"})
      else:
         return render(request, 'settings/passwd.html', {'err': 'Passwords do not Match', 'sess': request.session})
   else:
      return render(request, 'settings/passwd.html', {'sess': request.session})

@require_login
def theme(request):
   return render(request, 'settings/themeselector.html', {'sess': request.session})