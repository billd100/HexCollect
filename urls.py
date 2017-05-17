"""HexCollect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^missioncontrol/', admin.site.urls),
    url(r'^spotlight/', include('Spotlight.urls', namespace='spotlight')),
    url(r'^experiences/', include('Experiences.urls', namespace='experiences')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^blog/', include('Blog.urls', namespace='blog')),
    url(r'^u/', include('UserProfile.urls', namespace='userprofile')),
    url(r'^a/', include('allauth.urls')),
    url(r'^', include('Home.urls', namespace='hexcollect')),
]
