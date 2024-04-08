from django.db import models
import os
import uuid

def generate_filename(instance, filename):
   ext = filename.split('.')[-1]
   random_name = uuid.uuid4().hex
   return os.path.join('posts/', random_name + '.' + ext)

class Profile(models.Model):
   name = models.CharField(max_length = 30)
   email = models.CharField(max_length = 50, unique = True)
   mobile = models.CharField(max_length = 15)
   dob = models.DateField()
   username = models.CharField(max_length = 20, unique = True)
   password = models.CharField(max_length = 128)
   bio = models.TextField(blank = True)
   status = models.IntegerField(default = 1, blank = True)
   priv = models.IntegerField(default = 0)
   posts = models.IntegerField(default = 0, blank = True)
   followers = models.IntegerField(default = 0, blank = True)
   followings = models.IntegerField(default = 0, blank = True)
   image = models.ImageField(upload_to= 'user_img/', default= "blank_user.png")
   created = models.DateTimeField(auto_now_add=True)
   class Meta:
      db_table = "profile"

class Follow(models.Model):
   follower = models.IntegerField(default = 0, blank = False)
   followed = models.IntegerField(default = 0, blank = False)
   class Meta:
      db_table = "follow"

# class Group(models.Model):
#    admin = models.IntegerField(default = 0, blank = False)
#    image = models.ImageField(upload_to= 'group_img/', default= "blank_group.png")
#    description = models.TextField()
#    access = models.CharField(max_length=10)
#    created = models.DateTimeField(auto_now_add=True)
#    class Meta:
#       db_table = "group"

# class Membership(models.Model):
#    groupid = models.IntegerField(default = 0, blank = False)
#    userid = models.IntegerField(default = 0, blank = False)
#    role = models.CharField(max_length = 20)
#    class Meta:
#       db_table = "membership"

class Message(models.Model):
   sender = models.IntegerField(default = 0, blank = False)
   receiver = models.IntegerField(default = 0, blank = False)
   # grp = models.IntegerField(default = 0, blank = False)
   content = models.TextField()
   created = models.DateTimeField(auto_now_add=True)
   class Meta:
      db_table = "message"

class Post(models.Model):
   userid = models.IntegerField(default = 0, blank = False)
   description = models.TextField()
   file = models.FileField(upload_to=generate_filename)
   created = models.DateTimeField(auto_now_add=True)
   class Meta:
      db_table = "post"

class Likes(models.Model):
   userid = models.IntegerField(default = 0, blank = False)
   postid = models.IntegerField(default = 0, blank = False)
   class Meta:
      db_table = "likes"

class Comments(models.Model):
   userid = models.IntegerField(default = 0, blank = False)
   postid = models.IntegerField(default = 0, blank = False)
   created = models.DateTimeField(auto_now_add=True)
   class Meta:
      db_table = "comments"

class Report(models.Model):
   userid = models.IntegerField(default = 0, blank = False)
   postid = models.IntegerField(default = 0, blank = False)
   reason = models.CharField(max_length=30)
   content = models.TextField()
   created = models.DateTimeField(auto_now_add=True)
   class Meta:
      db_table = "report"