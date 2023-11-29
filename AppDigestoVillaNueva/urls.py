from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('decreto-crear/', views.DecretoCreateView.as_view(), name='decreto_create'),
    path('decreto-editar/<int:pk>/', views.DecretoUpdateView.as_view(), name='decreto_update'),
    path('decreto-listar/', views.DecretoListView.as_view(), name='decreto_list'),
    path('decreto-publicar/<int:pk>/', views.DecretoPublicarView.as_view(), name='decreto_public'),
    path('decreto-publicar-masivo', views.DecretoPublicarMasivoView.as_view(), name='decreto_public_masivo'),
    path('decreto-eliminar/<int:pk>/', views.DecretoDeleteView.as_view(), name='decreto_delete'),
    path('decreto-pdf/<int:pk>/', views.decreto_pdf_view, name='decreto_pdf'),
]