from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', login_required(index), name='index'),
    path('decreto-crear/', login_required(DecretoCreateView.as_view()), name='decreto_create'),
    path('decreto-editar/<int:pk>/', login_required(DecretoUpdateView.as_view()), name='decreto_update'),
    path('decreto-listar/', login_required(DecretoListView.as_view()), name='decreto_list'),
    path('decreto-publicar/<int:pk>/', login_required(DecretoPublicarView.as_view()), name='decreto_public'),
    path('decreto-publicar-masivo', login_required(DecretoPublicarMasivoView.as_view()), name='decreto_public_masivo'),
    path('decreto-eliminar/<int:pk>/', login_required(DecretoDeleteView.as_view()), name='decreto_delete'),
    path('decreto-pdf/<int:pk>/', login_required(decreto_pdf_view), name='decreto_pdf'),
    path('ordenanza-crear/', login_required(OrdenanzaCreateView.as_view()), name='ordenanza_create'),
    path('ordenanza-editar/<int:pk>/', login_required(OrdenanzaUpdateView.as_view()), name='ordenanza_update'),
    path('ordenanza-listar/', login_required(OrdenanzaListView.as_view()), name='ordenanza_list'),
    path('ordenanza-publicar/<int:pk>/', login_required(OrdenanzaPublicarView.as_view()), name='ordenanza_public'),
    path('ordenanza-publicar-masivo', login_required(OrdenanzaPublicarMasivoView.as_view()), name='ordenanza_public_masivo'),
    path('ordenanza-eliminar/<int:pk>/', login_required(OrdenanzaDeleteView.as_view()), name='ordenanza_delete'),
    path('ordenanza-pdf/<int:pk>/', login_required(ordenanza_pdf_view), name='ordenanza_pdf'),
    path('resolucion-crear/', login_required(ResolucionCreateView.as_view()), name='resolucion_create'),
    path('resolucion-editar/<int:pk>/', login_required(ResolucionUpdateView.as_view()), name='resolucion_update'),
    path('resolucion-listar/', login_required(ResolucionListView.as_view()), name='resolucion_list'),
    path('resolucion-publicar/<int:pk>/', login_required(ResolucionPublicarView.as_view()), name='resolucion_public'),
    path('resolucion-publicar-masivo', login_required(ResolucionPublicarMasivoView.as_view()), name='resolucion_public_masivo'),
    path('resolucion-eliminar/<int:pk>/', login_required(ResolucionDeleteView.as_view()), name='resolucion_delete'),
    path('resolucion-pdf/<int:pk>/', login_required(resolucion_pdf_view), name='resolucion_pdf'),
    path('declaracion-crear/', login_required(DeclaracionCreateView.as_view()), name='declaracion_create'),
    path('declaracion-editar/<int:pk>/', login_required(DeclaracionUpdateView.as_view()), name='declaracion_update'),
    path('declaracion-listar/', login_required(DeclaracionListView.as_view()), name='declaracion_list'),
    path('declaracion-publicar/<int:pk>/', login_required(DeclaracionPublicarView.as_view()), name='declaracion_public'),
    path('declaracion-publicar-masivo', login_required(DeclaracionPublicarMasivoView.as_view()), name='declaracion_public_masivo'),
    path('declaracion-eliminar/<int:pk>/', login_required(DeclaracionDeleteView.as_view()), name='declaracion_delete'),
    path('declaracion-pdf/<int:pk>/', login_required(declaracion_pdf_view), name='declaracion_pdf'),
    path('boletinoficial-crear', crear_boletin, name='boletinoficial_create'),
    path('boletinoficial/<int:pk>/', login_required(boletin_detail), name='boletinoficial_detail'),
    path('boletinoficial-listar/', login_required(BoletinOficialListView.as_view()), name='boletinoficial_list'),
    path('boletinoficial-pdf/<int:pk>/', login_required(boletin_pdf_view), name='boletinoficial_pdf'),
    path('boletinoficial-publicar/<int:pk>/', login_required(BoletinOficialPublicarView.as_view()), name='boletinoficial_public'),
    path('boletinoficial-eliminar/<int:pk>/', login_required(BoletinOficialDeleteView.as_view()), name='boletinoficial_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)