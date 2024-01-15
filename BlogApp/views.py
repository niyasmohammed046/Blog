from django.shortcuts import render
from . models import Post, Comments , Tag ,Profile
from . forms import CommentForm ,SubscribeForm
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count


def home(request):
    posts = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]  #the slicing is to show only three most view count post
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured = True)
    subscribe_form = SubscribeForm
    sub_message = None

    if featured_blog:
        featured_blog = featured_blog[0] #this is to the the first top one freatred blog
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            sub_message = 'Subscribed Successful'
            subscribe_form = SubscribeForm # this is to clear the form after the submission
    context = {
        'posts':posts,
        'top_post':top_post,
        'recent_post':recent_post,
        'subscribe_form':subscribe_form,
        'sub_message':sub_message,
        'featured_blog':featured_blog
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


def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    all_tags = Tag.objects.all()
    top_post = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2] #tags__ is from Post model ,we can use __in because its a foreignkey
    recent_post = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:2]
    context = {
        'tag':tag,
        'top_post':top_post,
        'recent_post':recent_post,
        'all_tags':all_tags,
    }
    return render(request,'app/tag.html',context)

def author_page(request,slug):
    profile = Profile.objects.get(slug=slug)
    top_post = Post.objects.filter(author = profile.user).order_by('-view_count')[0:2] # the author = author_profile.user , first author comes from the Post model and the second auther_profile.user comes from the Profile model
    recent_post = Post.objects.filter(author = profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    context = {
        'profile':profile,
        'top_post':top_post,
        'recent_post':recent_post,
        'top_authors':top_authors
    }
    return render(request,'app/author.html',context)
