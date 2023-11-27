from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.urls import reverse_lazy
from datetime import date
from django.db.models import Max
from .models import Decreto
from .forms import DecretoForm

# Create your views here.

class DecretoCreateView(CreateView):
    model = Decreto
    form_class = DecretoForm
    template_name = "decreto_create.html"
    success_url = reverse_lazy('decreto_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        # Obtiene el valor máximo de numero_decreto del año actual + 1
        today = date.today()
        year = today.year
        max_decreto = Decreto.objects.filter(anio=year).aggregate(Max('numero_decreto'))['numero_decreto__max']

        # Si no hay ningún decreto para el año actual, asigna 1 como valor predeterminado
        if max_decreto is None:
            max_decreto = 1
        else:
            max_decreto += 1

        # Devuelve un diccionario con el valor predeterminado para numero_decreto
        return {'numero_decreto': max_decreto}
    
    def form_valid(self, form):
        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class DecretoUpdateView(UpdateView):
    model = Decreto
    form_class = DecretoForm
    template_name = "decreto_edit.html"
    success_url = reverse_lazy('decreto_list')

    def form_valid(self, form):
        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class DecretoListView(ListView):
    model = Decreto
    template_name = "decreto_list.html"
    context_object_name = 'decretos'