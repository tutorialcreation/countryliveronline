from django.urls import path
from . import views

app_name = "lands"

urlpatterns = [
    path("", views.AddLand.as_view(), name="add_land"),
    path("property24/", views.PropertyScrapperView.as_view(), name="prop24_scrapper"),
]
