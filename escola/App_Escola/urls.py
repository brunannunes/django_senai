from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.abre_index, name='abre_index'),
   
   
]