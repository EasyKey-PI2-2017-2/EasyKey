from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views
from easykey.settings import DEBUG

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^key_code/$', views.key_code, name='key_code'),
    url(r'^key_cut/$', views.key_cut, name='key_cut'),
    url(r'^key_finish/$', views.key_finish, name='key_finish'),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),]
