from django.shortcuts import render,redirect , get_object_or_404
from . models import Post, Comments , Tag ,Profile ,WebsiteMeta
from . forms import CommentForm ,SubscribeForm , RegisterForm
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    posts = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]  #the slicing is to show only three most view count post
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured = True)
    subscribe_form = SubscribeForm
    sub_message = None
    websiteinfo = None

    if WebsiteMeta.objects.all().exists():
        websiteinfo = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0] #this is to the the first top one freatred blog
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            sub_message = 'Subscribed Successful'
            subscribe_form = SubscribeForm # this is to clear the form after the submission
    context = {
        'posts':posts,
        'top_post':top_post,
        'recent_post':recent_post,
        'subscribe_form':subscribe_form,
        'sub_message':sub_message,
        'featured_blog':featured_blog,
        'websiteinfo':websiteinfo
    }
    return render(request,'app/index.html',context)

@login_required
def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    view_comments = Comments.objects.filter(post=post ,comment_reply=None)
    form = CommentForm()

    #bookmark logic
    bookmarked = False
    if post.bookmarks.filter(id= request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked

    #like logic
    liked_post = False
    like_count = post.number_of_likes
    if post.likes.filter(id= request.user.id).exists():
        liked_post = True
    post_is_liked = liked_post

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

    #side bar post
    recent_posts = Post.objects.exclude(id = post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[0:3]
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id = post.id).filter(author=post.author)[0:3]

    context = {
        'post':post,
        'form':form,
        'view_comments':view_comments,
        'is_bookmarked':is_bookmarked,
        'post_is_liked':post_is_liked,
        'like_count':like_count,

        'recent_posts':recent_posts,
        'top_authors':top_authors,
        'tags':tags,
        'related_posts':related_posts
    }
    return render(request,'app/post.html',context)

@login_required
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

@login_required
def author_page(request,slug):
    profile = Profile.objects.get(slug=slug)
    top_post = Post.objects.filter(author = profile.user).order_by('-view_count')[0:2] # the author = author_profile.user , first author comes from the Post model and the second auther_profile.user comes from the Profile model
    recent_post = Post.objects.filter(author = profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')
    
    context = {
        'profile':profile,
        'top_post':top_post,
        'recent_post':recent_post,
        'top_authors':top_authors
    }
    return render(request,'app/author.html',context)


@login_required
def search_post(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'posts':posts,
        'search_query':search_query
        }
    return render(request,'app/search.html',context)

@login_required
def bookmark_post(request,slug):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page',args=[str(slug)]))

@login_required
def like_post(request,slug):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page',args=[str(slug)]))

@login_required
def all_bookmarked_post(request):
    all_bookmarked_post = Post.objects.filter(bookmarks=request.user)
    context = {
        'all_bookmarked_post':all_bookmarked_post
    }
    return render(request,'app/all_bookmarked_post.html',context)

@login_required
def all_posts(request):
    all_posts = Post.objects.all()
    context = {
        'all_posts':all_posts
    }
    return render(request,'app/all_post.html',context)

@login_required
def about_page(request):
    Website_about = WebsiteMeta.objects.all()[0]
    context = {'Website_about':Website_about}
    return render(request,'app/about.html',context)


#Register and Login

def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Success')
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request,'registration/login.html')
    
def logout_user(request):
    logout(request)
    return render(request,'registration/logout.html')

    

def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('login')
    context = {'form':form}
    return render(request,'registration/register.html',context)