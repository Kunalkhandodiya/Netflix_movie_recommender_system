from app import views
from django.urls import path

urlpatterns = [
    path("", views.recommend_view, name="recommend_view")
]