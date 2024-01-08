from django.shortcuts import render
from . models import Post


def home(request):
    pass

def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    context = {
        'post':post,
    }
    return render(request,'app/post.html',context)