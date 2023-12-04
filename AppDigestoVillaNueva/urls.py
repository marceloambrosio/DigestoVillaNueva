from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('home/', index, name='index'),
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
    path('resolucion-crear/', ResolucionCreateView.as_view(), name='resolucion_create'),
    path('resolucion-editar/<int:pk>/', ResolucionUpdateView.as_view(), name='resolucion_update'),
    path('resolucion-listar/', ResolucionListView.as_view(), name='resolucion_list'),
    path('resolucion-publicar/<int:pk>/', ResolucionPublicarView.as_view(), name='resolucion_public'),
    path('resolucion-publicar-masivo', ResolucionPublicarMasivoView.as_view(), name='resolucion_public_masivo'),
    path('resolucion-eliminar/<int:pk>/', ResolucionDeleteView.as_view(), name='resolucion_delete'),
    path('resolucion-pdf/<int:pk>/', resolucion_pdf_view, name='resolucion_pdf'),
    path('declaracion-crear/', DeclaracionCreateView.as_view(), name='declaracion_create'),
    path('declaracion-editar/<int:pk>/', DeclaracionUpdateView.as_view(), name='declaracion_update'),
    path('declaracion-listar/', DeclaracionListView.as_view(), name='declaracion_list'),
    path('declaracion-publicar/<int:pk>/', DeclaracionPublicarView.as_view(), name='declaracion_public'),
    path('declaracion-publicar-masivo', DeclaracionPublicarMasivoView.as_view(), name='declaracion_public_masivo'),
    path('declaracion-eliminar/<int:pk>/', DeclaracionDeleteView.as_view(), name='declaracion_delete'),
    path('declaracion-pdf/<int:pk>/', declaracion_pdf_view, name='declaracion_pdf'),
    path('boletinoficial-crear', crear_boletin, name='boletin_create'),
    path('boletinoficial/<int:pk>/', boletin_detail, name='boletin_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)