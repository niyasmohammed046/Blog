from django.shortcuts import render
from . models import Post, Comments
from . forms import CommentForm
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

def home(request):
    posts = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]  #the slicing is to show only three most view count post
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    context = {
        'posts':posts,
        'top_post':top_post,
        'recent_post':recent_post
    }
    return render(request,'app/index.html',context)

def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    view_comments = Comments.objects.filter(post=post ,comment_reply=None)
    form = CommentForm()

    if request.POST:
        commentform = CommentForm(request.POST)     #comment section
        if commentform.is_valid:
            reply_obj = None
            #saving the reply
            if request.POST.get('reply'):   #checking the request has name="reply" from html
                reply = request.POST.get('reply')
                reply_obj = Comments.objects.get(id=reply)
                if reply_obj:
                    cmt_reply = commentform.save(commit=False)
                    cmt_reply.comment_reply = reply_obj
                    cmt_reply.post = post
                    cmt_reply.save()
                    return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))
            else:
                comment = commentform.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)  # this is getting from the input hidden tag on html
                comment.post = post   # this post is a foreignkey
                comment.save()
                return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))   #the kwargs step is to get the slug on the page and we are passing it in the dictionary
        

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {
        'post':post,
        'form':form,
        'view_comments':view_comments
    }
    return render(request,'app/post.html',context)
