"""
URL configuration for toyfactory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from toyfactory_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',                              views.index,          name='index'),
    re_path(r'^toy/list$',                views.toys_list,      name='toys_list'),
    re_path(r'^toy/list/(?P<toy_type>[-\w]+)$', views.toys_list, name='toys_list_by_type'),
    re_path(r'^toy/detail/(?P<pk>\d+)$', views.toy_details, name='toy_detail'),
    re_path(r'^news/$',                   views.news_list_view, name='news_list'),
    re_path(r'^news/detail/(?P<pk>\d+)$', views.news_detail_view, name='news_detail'),
    re_path(r'^account/register_client$', views.register_client, name='register_client'),
    re_path(r'^account/login_client$',    views.login_client,   name='login_client'),
    re_path(r'^account/login_employee$',  views.login_employee, name='login_employee'),
    re_path(r'^account/logout$',          views.logout_view,    name='logout'),
    re_path(r'^account/profile/(?P<pk>\d+)$', views.profile_view, name='profile'),
    re_path(r'^account/update_profile/(?P<pk>\d+)$', views.update_profile_view, name='update_profile'),
    path('promocodes/', views.promocodes, name='promocodes'),
    re_path(r'^feedbacks/$',  views.feedbacks_view,  name='feedbacks'),
    re_path(r'^feedbacks/add$', views.add_feedback_view, name='add_feedback'),
    path('policy/',     views.policy,     name='policy'),
    path('vacations/',  views.vacations,  name='vacations'),
    path('termines/',   views.termines,   name='termines'),
    path('about/',      views.about,      name='about')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)