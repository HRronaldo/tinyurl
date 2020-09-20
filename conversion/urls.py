from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lts/', views.long_2_short, name='lts'),
    path('<str:short_key>/', views.short_2_long, name="short_to_long"),
]