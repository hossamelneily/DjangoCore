
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url

urlpatterns = [


    url(r'^', include("blog.urls", namespace="blog")),
    path('admin/', admin.site.urls),
]
