from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from ..models import *
# from .decorators import *

def test(request):
   if request.method == 'POST':
      return render(request, 'test.html', {'val': make_password(request.POST['txt'])})
   else:
      return render(request, 'test.html')

def adder(request):
   if request.method == "POST":
      if "user" in request.POST:
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
         return render(request, 'adder.html', {'loc': 1, 'msg': msg})
      if "post" in request.POST:
         pst = Post.objects.create(
            userid = request.POST['uid'],
            description = request.POST['desc'],
            file = request.FILES['filee']
         )
         try:
            pst.save()
            msg = "Success"
         except:
            msg="Failed"
         return render(request, 'adder.html', {'loc': 2, 'msg': msg})
   else:
      return render(request, 'adder.html')