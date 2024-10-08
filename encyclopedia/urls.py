from django.urls import path
from django.conf.urls import handler404
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.entry, name='entry'),
    path('wiki/<str:title>/edit/', views.edit, name='edit'),
    path('search/', views.search, name='search'),
    path('new/', views.new, name='new'),
    path('random/', views.random_page, name='random'),
]

handler404 = 'encyclopedia.views.custom_404'