from django.conf.urls import url

from . import views

app_name = 'umbrella_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /umbrella_system/201606/date/
    url(r'^(?P<dates>[0-9]+)/date/$', views.date, name='date'),
    url(r'^room/$', views.room, name='room'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_go/$', views.login_go, name='login_go'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<dates>[0-9]+)/(?P<room>[0-9]+)/(?P<time>[0-9]+)/yoyaku/$', views.yoyaku, name='yoyaku'),
    url(r'^(?P<dates>[0-9]+)/(?P<room>[0-9]+)/(?P<time>[0-9]+)/yoyaku_del/$', views.yoyaku_del, name='yoyaku_del'),
    url(r'^yoyaku_touroku/$', views.yoyaku_touroku, name='yoyaku_touroku'),
    url(r'^yoyaku_del_go/$', views.yoyaku_del_go, name='yoyaku_del_go'),
    url(r'^(?P<dates>[0-9]+)/zikanwari/$', views.zikanwari, name='zikanwari'),
]