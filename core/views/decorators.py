from django.shortcuts import render, redirect

# from .__init__ import signin
# Hint for idiots: don't use the above line (circular import)


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