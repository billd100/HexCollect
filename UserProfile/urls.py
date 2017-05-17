from django.conf.urls import url
from . import views

app_name = 'userprofile'
urlpatterns = [
	url(r'^update_profile/$', views.update_profile, name="update_profile"),
	url(r'^update_conditions/', views.condition, name="update_conditions"),
	url(r'^(?P<user_name>[-\w]+)/$', views.profile, name="profile"),
		url(r'^(?P<username>[-\w]+)/journal/$', views.journal, name="journal"),
	]