"""Experiences URL Configuration"""

from . import views
from django.conf.urls import url

app_name = 'blog'
urlpatterns = [
	url(r'^$', views.blog, name='blog'),
	url(r'^(?P<slug>[-\w]+)/', views.blog_post, name='blog_post'),
]