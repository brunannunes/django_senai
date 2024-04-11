from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro')
   
]