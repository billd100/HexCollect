from . import views
from django.conf.urls import url

urlpatterns = [
	url(r'^about/$', views.about, name="about"),
	url(r'^about/user_agreement/', views.user_agreement, name="user_agreement"),
	url(r'^$', views.home_page, name="hexcollect"),
	]