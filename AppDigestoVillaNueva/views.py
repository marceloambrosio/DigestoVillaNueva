from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
    
    def get_queryset(self):
        return Decreto.objects.filter(eliminado=False).order_by('-anio', '-numero_decreto')

class DecretoDeleteView(UpdateView):
    model = Decreto
    fields = ['eliminado']

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.eliminado = True
        self.object.save()
        return redirect('decreto_list')


def decreto_pdf_view(request, pk):
    decreto = get_object_or_404(Decreto, pk=pk)
    
    with open(decreto.archivo_pdf.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        filename = 'Decreto-{0}-{1:04d}.pdf'.format(decreto.anio, decreto.numero_decreto)
        response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
        return response