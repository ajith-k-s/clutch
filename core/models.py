from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50, unique = True)
    mobile = models.CharField(max_length = 15)
    dob = models.DateField()
    username = models.CharField(max_length = 20, unique = True)
    password = models.CharField(max_length = 128)
    status = models.IntegerField(default = 1, blank = True)
    posts = models.IntegerField(default = 0, blank = True)
    flowr = models.IntegerField(default = 0, blank = True)
    flows = models.IntegerField(default = 0, blank = True)
    u_img = models.ImageField(upload_to= 'user_img', default= "blank_user.png")
    class Meta:
        db_table = "user"
        
# class Post(models.Model):