from django.conf.urls import include,url
from . import views
from django.views.generic.base import TemplateView

from .views import home,detail,create,update,delete,UsingTemplateView,BlogListView,BlogCreateView,BlogUpdateView,BlogDeleteView,BlogDetailView

app_name="blog"
urlpatterns = [

   url(r'^$',home,name="home"),
   url(r'^list/$', BlogListView.as_view(), name="list"),
   # url(r'^about/$', TemplateView.as_view(template_name='about.html'), name="home"),

   url(r'^about/$', UsingTemplateView.as_view(), name="about"),



   url(r'^(?P<id>\d+)$',detail,name="detail"),
   url(r'^(?P<id>\d+)/cbv',BlogDetailView.as_view(),name="detail2"),


   url(r'^(?P<id>\d+)/update$',BlogUpdateView.as_view(),name="update"),

   url(r'^create/$',create,name="create"),

   url(r'^createCBV/$',BlogCreateView.as_view(),name="create2"),


   url(r'^(?P<id>\d+)/edit$', update, name="update"),
   url(r'^(?P<id>\d+)/delete', delete, name="delete"),
   url(r'^(?P<id>\d+)/CBVDelete', BlogDeleteView.as_view(), name="delete2"),
]