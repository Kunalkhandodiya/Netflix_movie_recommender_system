from django.contrib import admin
from django.urls import path
from app import views
from django.views.generic import TemplateView

urlpatterns = [
      
    path("", TemplateView.as_view(template_name="app/templates/index.html"), name="index"),
    path("database/",views.database, name="database"),
    path("delete/",views.delete, name="delete"),
    path("insert/",views.insert, name="insert"),
    path("update/",views.update, name="update"),  


    path("rest/", TemplateView.as_view(template_name="app/templates/rest_index.html"), name="rest_api"),
    path("rest_database/",views.rest_database, name="rest_database"),
    path("rest_delete/<int:pk>/",views.rest_delete.as_view(), name="rest_delete"),
    path("rest_insert/",views.rest_insert, name="rest_insert"),
    path("rest_update/<int:pk>",views.rest_update.as_view(), name="rest_update"),

]