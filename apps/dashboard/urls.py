from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login', views.login),
    url(r'^register',views.register),
    url(r'^wall',views.wallPg),
    url(r'^logout', views.logout),
    url(r'^createPost', views.createPost),
    url(r'^createComment', views.createComment),
    url(r'^delete/post/(?P<post_id>\d+)', views.deletePost),
    url(r'^delete/comment/(?P<comment_id>\d+)', views.deleteComment),

]