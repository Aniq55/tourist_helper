from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Home Page
    url(r'^$', views.index, name='index'),
    #url(r'^submit/$',views.submitit, name='submitit'),
]
