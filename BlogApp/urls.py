from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('post/<slug:slug>/',views.post_page,name="post_page"),
    path('tag/<slug:slug>/',views.tag_page,name="tag_page"),
    path('author/<slug:slug>/',views.author_page,name='author_page'),
    path('search/',views.search_post,name="search"),
    path('about/',views.about_page,name='about'),
    path('bookmark/<slug:slug>/',views.bookmark_post,name='bookmark'),
    path('like/<slug:slug>/',views.like_post,name='like'),
    path('bookmarked_post/',views.all_bookmarked_post,name='bookmarked_post'),
    path('all_posts/',views.all_posts,name='all_posts'),

    #login and register
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),

]