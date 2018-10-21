from django.urls import path

from . import views

urlpatterns = [
    path('', views.spares, name='index'),
    path('json.json', views.requests, name='json')
]