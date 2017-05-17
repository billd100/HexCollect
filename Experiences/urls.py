"""Experiences URL Configuration"""

from . import views
from django.conf.urls import url

app_name = 'experiences'
urlpatterns = [
    url(r'^share/', views.share_experience, name='share_experience'),
    url(r'^activity/$', views.activity, name='activity'),
    	url(r'^activity/(?P<page>\d+)/', views.activity, name='activity_page'),
	url(r'^(?P<id>\d+)/$', views.experience_detail, name='experience_detail'),
    	 url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/', views.experience_detail, name='experience_detail_slug'),
    	 url(r'^(?P<id>\d+)/update', views.update_experience, name='update_experience'),
    	 url(r'^(?P<id>\d+)/edit', views.edit_experience, name='edit_experience'),
    url(r'^search/', views.experience_search, name='experience_search'),
    url(r'^delete_own_comment/(?P<message_id>\d+)/', views.delete_own_comment, name='delete_own_comment'),
    url(r'^$', views.experiences, name='experiences'),
]