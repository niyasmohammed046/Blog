from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100,unique=True)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True,upload_to="Post Images")
    

