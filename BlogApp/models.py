from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True,upload_to="User Profile")
    slug = models.SlugField(max_length=100,unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args , **kwargs): #this is to generate slug automatically
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile,self).save(*args,**kwargs)
    def __str__(self):
        return self.user.first_name


class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50,unique=True)

    def save(self, *args , **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.name
  

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100,unique=True)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True,upload_to="Post Images")
    tags = models.ManyToManyField(Tag,blank=True,related_name='post')
    view_count = models.IntegerField(null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title
    

class Comments(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    auther = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) # this will change later
    comment_reply = models.ForeignKey('self', on_delete=models.DO_NOTHING ,null=True ,blank=True,related_name='replies') #this relate name is to get the all comment under one post, or else we need to use _set method

