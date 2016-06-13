from django.conf.urls import url

from . import views

app_name = 'umbrella_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /umbrella_system/201606/date/
    url(r'^(?P<dates>[0-9]+)/date/$', views.date, name='date'),
]