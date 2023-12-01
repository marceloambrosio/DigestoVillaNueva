from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('decreto-crear/', DecretoCreateView.as_view(), name='decreto_create'),
    path('decreto-editar/<int:pk>/', DecretoUpdateView.as_view(), name='decreto_update'),
    path('decreto-listar/', DecretoListView.as_view(), name='decreto_list'),
    path('decreto-publicar/<int:pk>/', DecretoPublicarView.as_view(), name='decreto_public'),
    path('decreto-publicar-masivo', DecretoPublicarMasivoView.as_view(), name='decreto_public_masivo'),
    path('decreto-eliminar/<int:pk>/', DecretoDeleteView.as_view(), name='decreto_delete'),
    path('decreto-pdf/<int:pk>/', decreto_pdf_view, name='decreto_pdf'),
]