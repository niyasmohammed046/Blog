from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('post/<slug:slug>/',views.post_page,name="post_page"),
    path('tag/<slug:slug>/',views.tag_page,name="tag_page"),
    path('author/<slug:slug>/',views.author_page,name="author_page"),
]