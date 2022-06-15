from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.GameListAPIView.as_view()),
    path('game/<str:slug>', views.GameDetailsAPIView.as_view()),
]
