from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import urls as auth_urls
urlpatterns = [
    url(r'^criteria/$', views.movie_criteria, name='movie_criteria'),
    url(r'^criteria_weight/$', views.movie_criteria_weight, name='movie_criteria_weight'),
]