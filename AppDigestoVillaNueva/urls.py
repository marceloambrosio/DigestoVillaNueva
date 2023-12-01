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
    path('ordenanza-crear/', OrdenanzaCreateView.as_view(), name='ordenanza_create'),
    path('ordenanza-editar/<int:pk>/', OrdenanzaUpdateView.as_view(), name='ordenanza_update'),
    path('ordenanza-listar/', OrdenanzaListView.as_view(), name='ordenanza_list'),
    path('ordenanza-publicar/<int:pk>/', OrdenanzaPublicarView.as_view(), name='ordenanza_public'),
    path('ordenanza-publicar-masivo', OrdenanzaPublicarMasivoView.as_view(), name='ordenanza_public_masivo'),
    path('ordenanza-eliminar/<int:pk>/', OrdenanzaDeleteView.as_view(), name='ordenanza_delete'),
    path('ordenanza-pdf/<int:pk>/', ordenanza_pdf_view, name='ordenanza_pdf'),
]