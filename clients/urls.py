from django.urls import path
from . import views

urlpatterns = [
    path('yellowpages/', views.YellowPagesScrapperView.as_view()),
    path('facebook/', views.FacebookScrapperView.as_view()),
]
