from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from ..models import *

from .decorators import *
from .admin import *
from .settings import *
from .user import *
from .test import *
from .chat import *
# from .DB import DbConnection
# dbobj=DbConnection(host="localhost",user="root",passwd="",database="clutch",port=3306)




##########     Error Handler
def page_not_found(request, exception=None):
   return render(request, '404.html')



##########     JSON Response
def checkUsr(request):        # check whether username is available of not
   if request.method == 'GET':
      username = request.GET.get('username', None)
      if username:
         if 'username' in request.session and username == request.session['username']:
            return JsonResponse({'exists': False})
         else:
            rec = Profile.objects.filter(username=username).count()
            return JsonResponse({'exists': rec > 0})
      else:
         return JsonResponse({'error': 'Profilename parameter missing'}, status=400)
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

def checkLike(request):
   if request.method == 'GET':
      pid = request.GET.get('pid', None)
      rec = Likes.objects.filter(userid = request.session['uid'], postid=pid)
      if rec.count() == 1:
         return JsonResponse({'like': True})
      else:
         return JsonResponse({'like': False})
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=404)
   
def toggleLike(request):
   if request.method == 'GET':
      pid = request.GET.get('pid', None)
      rec = Likes.objects.filter(userid = request.session['uid'], postid=pid)
      if rec.count() == 1:
         try:
            Likes.objects.get(userid = request.session['uid'], postid=pid).delete()
            return JsonResponse({'like': False})
         except:
            return JsonResponse({'like': True})
      else:
         try:
            Likes.objects.create(userid = request.session['uid'], postid=pid).save()
            return JsonResponse({'like': True})
         except:
            return JsonResponse({'like': False})
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=404)
   
def toggleFollow(request):
   if request.method == 'GET':
      uid = request.GET.get('uid', None)
      rec = Follow.objects.filter(follower = request.session['uid'], followed=uid)
      usr = Profile.objects.get(id=uid)
      if rec.count() == 1:
         try:
            Follow.objects.get(follower = request.session['uid'], followed=uid).delete()
            usr.followers -= 1
            usr.save()
            return JsonResponse({'follow': False, 'count': usr.followers})
         except:
            return JsonResponse({'follow': True, 'count': usr.followers})
      else:
         try:
            Follow.objects.create(follower = request.session['uid'], followed=uid).save()
            usr.followers += 1
            usr.save()
            return JsonResponse({'follow': True, 'count': usr.followers})
         except:
            return JsonResponse({'follow': False, 'count': usr.followers})
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=404)

def checkFollow(request):
   if request.method == 'GET':
      uid = request.GET.get('uid', None)
      rec = Follow.objects.filter(follower = request.session['uid'], followed=uid)
      if rec.count() == 1:
         return JsonResponse({'follow': True})
      else:
         return JsonResponse({'follow': False})
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=404)




##########     Base
@require_login
def index(request):
   if request.session['username'] =='admin':
      return render(request,'admin/home.html', {'sess': request.session})
   else:
      return redirect(feed)


def signin(request):
   if request.method == 'POST':
      username=request.POST["username"]
      password=request.POST["password"]
      rec=Profile.objects.filter(username=username)
      if rec.count()>0:
         rec = Profile.objects.get(username=username)
         if check_password(password, rec.password):
            if rec.status == 0:
               return render(request,'signin.html', {'err': 1})
            else:
               request.session['uid'] = rec.id
               request.session['username'] = rec.username
               request.session['profile_image'] = rec.image.url
               return redirect(index)
         else:
            return render(request,'signin.html', {'err': 0})
      else:
         return render(request,'signin.html', {'err': 0})
   else:
      return render(request,'signin.html')


def signup(request):
   if request.method == 'POST':
      usr = Profile.objects.create(
         name = request.POST['name'],
         email = request.POST['email'],
         mobile = request.POST['mobile'],
         dob = request.POST['dob'],
         username = request.POST['username'],
         password = make_password(request.POST['password'])
      )
      try:
         usr.save()
         return redirect(signin)
      except:
         errmsg='Profile Registration Failed'
         return render(request,'signup.html',{'errmsg':errmsg})
   else:return render(request,'signup.html')


def signout(request):
   logout(request)
   return redirect('signin')