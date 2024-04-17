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
   pst = Post.objects.filter(userid=pro.id)
   if username == request.session['username']:
      isusr = True
   else:
      isusr = False
   if pst.count() == 0:
      res = 2
   else:
      res = 0
   cmt = 0
   cmts = 0
   if 'cmt' in request.GET:
      cmt = int(request.GET['cmt'])
      rec = Comments.objects.filter(postid=cmt).select_related('userid').values('id', 'userid__name', 'userid__username', 'userid__image', 'content', 'created')
      if rec.count() > 0:
         rec = Comments.objects.filter(postid=cmt)
         cmts = []
         for comment in rec:
            profile = Profile.objects.get(id=comment.userid_id)
            comment_dict = {
               'id': comment.id,
               'userid': comment.userid_id,
               'username': profile.username,  # Add username from Profile
               'image': profile.image.url,    # Add image URL from Profile
               'content': comment.content,
               'created': comment.created
            }
            cmts.append(comment_dict)
            
   if request.method == 'POST' and 'txt' in request.POST and request.POST['txt'] != '':
      pid = int(request.POST['pid'])
      comment = Comments.objects.create(
         userid=pro,
         postid=pid,
         content=request.POST['txt']
      )
      try:
         comment.save()
         print("comment added success")
      except:
         print("comment failed")
   return render(request, 'user/profile.html', {'pro': pro, 'res': res, 'pst': pst, 'isusr': isusr, 'sess': request.session, 'cmt': cmt, 'cmts': cmts})

@require_login
def addPost(request):
   if request.method == 'POST':
      pst = Post.objects.create(
         userid = request.session['uid'],
         description = request.POST['desc'],
      )
      if 'filee' in request.FILES:
         ext = request.FILES['filee'].name.split('.')[-1]
         imgExt = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
         vidExt = ["mp4", "webm"]
         if ext in imgExt:
            pst.file = request.FILES['filee']
            pst.filetype = 'img'
         elif ext in vidExt:
            pst.file = request.FILES['filee']
            pst.filetype = 'vid'
      try:
         pst.save()
         msg = "Success"
      except:
         msg="Failed"
         return render(request, 'user/addpost.html', {'sess': request.session, "msg": msg}) 
      return redirect(reuser)
   else:
      return render(request, 'user/addpost.html', {'sess': request.session})

@require_login
def search(request):
   if request.method == 'GET' and 's' in request.GET and request.GET['s'] != '':
      records = Profile.objects.filter(name__icontains=request.GET['s'])
      if records.count() == 0:
         records = 1
      return render(request, 'user/search.html', {'key': request.GET['s'], 'records': records,'sess': request.session})
   else:
      return render(request, 'user/search.html', {'sess': request.session})

@require_login
def followers(request):
   rel = Follow.objects.filter(followed=request.session['uid']).values_list('follower', flat=True)
   records = []
   if rel.count() == 0:
      records = 1
   else:
      for r in rel:
         profile = Profile.objects.get(id=r)
         r_dict = {
            'id': profile.id,
            'username': profile.username,
            'image': profile.image.url,
         }
         records.append(r_dict)
   return render(request, 'user/followers.html', {'records': records,'sess': request.session})

@require_login
def followings(request):
   rel = Follow.objects.filter(follower=request.session['uid']).values_list('followed', flat=True)
   records = []
   if rel.count() == 0:
      records = 1
   else:
      for r in rel:
         profile = Profile.objects.get(id=r)
         r_dict = {
            'id': profile.id,
            'username': profile.username,
            'image': profile.image.url,
         }
         records.append(r_dict)
   return render(request, 'user/followings.html', {'records': records,'sess': request.session})