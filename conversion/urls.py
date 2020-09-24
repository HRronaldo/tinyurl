from django.urls import path

from . import views


app_name = "conversion"
urlpatterns = [
    path('', views.index, name='index'),
    path('lts/', views.long_2_short_v2, name='long_2_short'),
    path('<str:short_key>/', views.short_2_long_v2, name="short_to_long"),
]