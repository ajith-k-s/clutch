from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import *
from .DB import DbConnection

dbobj=DbConnection(host="localhost",user="root",passwd="",database="clutch",port=3306)



###########################
###     Decorators      ###
def require_login(fn):
   def wrapper(request, *args, **kwargs):
      if 'uid' not in request.session:
         return redirect(signin)
      else:
         return fn(request, *args, **kwargs)
   return wrapper

def require_admin(fn):
   def wrapper(request, *args, **kwargs):
      if request.session['username'] == 'admin':
         return fn(request, *args, **kwargs)
      else:
         return render(request, '404.html')
   return wrapper
###     Decorators      ###
###########################



###########################
###    Error Handler    ###
def page_not_found(request, exception=None):
   return render(request, '404.html')
###    Error Handler    ###
###########################



###########################
###    JSON Response    ###
def checkUsr(request):        # check whether username is available of not
   if request.method == 'GET':
      username = request.GET.get('username', None)
      if username:
         rec = Profile.objects.filter(username=username).count()
         return JsonResponse({'exists': rec > 0})
      else:
         return JsonResponse({'error': 'Profilename parameter missing'}, status=400)
   else:
      return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
###    JSON Response    ###
###########################



###########################
###         Base        ###
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
###         Base        ###
###########################



###########################    
###      User page      ###
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
###      User page      ###
###########################



###########################
###       Settings      ###
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
         if check_password(request.POST['cpass'], usr.password):
            usr.password = make_password(request.POST['npaswd'])
         try:
            usr.save()
            request.session['username'] = usr.username
            err = '0'
         except:
            err = '1'
         usr = Profile.objects.get(id = request.session['uid'])
         return render(request, 'account.html', {'usr': usr, 'err': err, 'sess': request.session})
      elif request.POST['action'] == 'cancel':
         return render(request, 'settings/account.html', {'usr': usr, 'sess': request.session})
   else:
      return render(request, 'settings/account.html', {'usr': usr, 'sess': request.session})

@require_login
def theme(request):
   return render(request, 'settings/themeselector.html', {'sess': request.session})
###       Settings      ###
###########################



###########################    
###      Admin page     ###
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
###      Admin page     ###
###########################



###########################
###         Test        ###
def test(request):
   if request.method == 'POST':
      return render(request, 'test.html', {'val': make_password(request.POST['txt'])})
   else:
      return render(request, 'test.html')

def adder(request):
   if request.method == "POST":
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
         msg = "Success"
      except:
         msg="Failed"
      return render(request, 'adder.html', {'msg': msg})
   else:
      return render(request, 'adder.html')