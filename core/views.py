from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import logout
from .DB import DbConnection

dbobj=DbConnection(host="localhost",user="root",passwd="",database="clutch",port=3306)

def index(request):
	if 'uid' not in request.session:
		return redirect(signin)
	if request.session['username'] =='admin':
		return render(request,'admin/home.html')
	else:
		return render(request,'user/feed.html')

def signin(request):
	if request.method == 'POST':
		username=request.POST["username"]
		password=request.POST["password"]
		rec=User.objects.filter(username=username)
		if rec.count()>0:
			rec = User.objects.get(username=username)
			if check_password(password, rec.password):
				if rec.status == 0:
					return render(request,'signin.html', {'err': 1})
				else:
					request.session['uid'] = rec.id
					request.session['username'] = rec.username
					return redirect(index)
			else:
				return render(request,'signin.html', {'err': 0})
		else:
			return render(request,'signin.html', {'err': 0})
	else:
		return render(request,'signin.html')

def signup(request):
	if request.method == 'POST':
		usr = User.objects.create(
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
			errmsg='User Registration Failed'
			return render(request,'signup.html',{'errmsg':errmsg})
	else:
	 	return render(request,'signup.html')
	 
def signout(request):
	logout(request)
	return redirect('signin')



#########################    
###     Admin page    ###
#########################
def users(request):
	usrs=User.objects.all()
	return render(request,'admin/users.html',{'usrs':usrs})

def editusr(request, id):
	login = User.objects.get(id=id)
	return render(request,'admin/editusr.html', {'login':login})

def delusr(request, username):
	login = User.objects.get(username=username)
	login.delete()
	return redirect(users)



#########################    
###     User page     ###
#########################
def feed(request):
	return render(request, 'user/feed.html')




def test(request):
   if request.method == 'POST':
      return render(request, 'test.html', {'val': make_password(request.POST['txt'])})
   else:
      return render(request, 'test.html')