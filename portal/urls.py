"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from basic import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^searchfriend/$', views.search, name='search'),
    url(r'^addfriend/$', views.add_friend, name='add_friend'),
    url(r'^hangoutupdate/$', views.message_aa_gaya, name='send_message'),
    url(r'^fetchupdate/$', views.check_message, name='fetch_message'),
]
