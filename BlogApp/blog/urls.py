from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.urls import re_path, path
from blog.views import *

urlpatterns = [
    # post views
    # re_path(r'^$', post_list, name='post_list'),
    re_path(r'^$', PostListView.as_view(), name='home'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        post_detail,
        name='post_detail'),
    # re_path(r'^login/$', user_login, name='login'),
    re_path(r'^login/$', LoginView.as_view(
        template_name='blog/account/login.html'), 
        name="login"
    ),
    re_path(r'^$', dashboard, name='dashboard'),
    re_path(r'^logout/$', LogoutView.as_view(
        template_name='blog/account/logout.html'
        ), name="logout"
    ),
    re_path(r'^logout-then-login/$',
        logout_then_login,
        name='logout_then_login'
    ),
    
    re_path(r'^about/', about, name="about"),
    re_path(r'^create/', create, name="create"),
    re_path(r'^register/$', register, name='register'),
    re_path(r'^user_edit/$', user_edit, name='user_edit'),
    re_path(r'^user_profile/', user_profile, name='user_profile'),

    path('delete/<int:id>/', delete, name="delete"),
    path('edit/<int:id>/', edit, name="edit"),
    
]