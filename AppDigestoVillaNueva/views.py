from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.urls import reverse_lazy
from .models import Decreto
from .forms import DecretoForm

# Create your views here.

class DecretoCreateView(CreateView):
    model = Decreto
    form_class = DecretoForm
    template_name = "decreto_create.html"
    success_url = reverse_lazy('decreto_list')

class DecretoUpdateView(UpdateView):
    model = Decreto
    form_class = DecretoForm
    template_name = "decreto_edit.html"
    success_url = reverse_lazy('decreto_list')

class DecretoListView(ListView):
    model = Decreto
    template_name = "decreto_list.html"
    context_object_name = 'decretos'