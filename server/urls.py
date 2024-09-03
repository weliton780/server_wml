from django.urls import path
from . import views

urlpatterns = [
    path('dados/', views.listar_dados, name='listar_dados'),  # URL para listar dados
    path('model_ia/', views.inferencia_model_ia, name='inferencia_model_ia'),  # URL para a inferência do modelo IA
]
