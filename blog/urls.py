from django.conf.urls import include,url
from . import views

from .views import home,detail,create,update,delete

app_name="blog"
urlpatterns = [

   url(r'^$',home,name="home"),
   url(r'^(?P<id>\d+)$',detail,name="detail"),
   url(r'^create/$',create,name="create"),
   url(r'^(?P<id>\d+)/edit$', update, name="update"),
   url(r'^(?P<id>\d+)/delete', delete, name="delete"),
]