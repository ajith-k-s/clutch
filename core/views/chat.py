from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Max
from .decorators import require_login
from ..models import Message, Profile

def getUserList(uid):
   sender = Message.objects.filter(sender=uid).values_list('receiver', flat=True).distinct()
   receiver = Message.objects.filter(receiver=uid).values_list('sender', flat=True).distinct()
   unique_values = set((list(sender)+list(receiver)))
   if not unique_values:
      return
   userid = sorted(unique_values, key=lambda x: Message.objects.filter(Q(sender=x, receiver=uid) | Q(receiver=x, sender=uid)).aggregate(latest_created=Max('created'))['latest_created'], reverse=True)
   users = []
   for u in userid:
      p = Profile.objects.get(id=u)
      usr_dict = {
         'id': p.id,
         'username': p.username,
         'image': p.image.url,
      }
      users.append(usr_dict)
   return users

# def sendMsg(request):
#    if request.method == 'GET':
#       uid = request.GET.get('uid', None)
#       try:
#          msg = Message.objects.create(sender = request.session['uid'], receiver = uid, content = request.GET['txt']).save()
#          return JsonResponse({'isSend': True})
#       except:
#          return JsonResponse({'isSend': False})
#    else:
#       return JsonResponse({'error': 'Only GET method is allowed'}, status=404)

@require_login
def chatView(request, username=""):
   if username != "":
      u = Profile.objects.get(username=username)
      # Retrieve messages related to the current user and the u passed in the URL
      messages = Message.objects.filter(Q(sender=request.session['uid'], receiver=u.id) | Q(sender=u.id, receiver=request.session['uid']))
      # Pass messages and u to the template
      if request.method == 'POST':
         msg = Message.objects.create(
            sender = request.session['uid'],
            receiver = u.id,
            content = request.POST['txt']
         )
         try:
            msg.save()
            errmsg = "Success"
         except:
            errmsg = "failed"
      return render(request, 'chat/chat.html', {'sess': request.session, 'messages': messages, 'u': u, 'users': getUserList(request.session['uid'])})
   else:
      return render(request, 'chat/chat.html', {'sess': request.session, 'users': getUserList(request.session['uid'])})