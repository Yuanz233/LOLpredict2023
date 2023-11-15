from django.contrib import admin
from django.urls import path,include
from predict import views

urlpatterns = [
    path("",views.get_home_page,name="LOL-predict"),
    path("result/",views.predict_view,name="predict-view"),
]