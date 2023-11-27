from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('decreto-crear/', views.DecretoCreateView.as_view(), name='decreto_create'),
    path('decreto-editar/<int:pk>/', views.DecretoUpdateView.as_view(), name='decreto_update'),
    path('decreto-listar/', views.DecretoListView.as_view(), name='decreto_list'),
]