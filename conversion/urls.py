from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lts/', views.long_2_short, name='lts'),
]