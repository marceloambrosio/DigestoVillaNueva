from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import date
from django.db.models import Max
from ..models import Ordenanza
from ..forms import OrdenanzaForm
from datetime import datetime

# Create your views here.

class OrdenanzaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ordenanza
    form_class = OrdenanzaForm
    template_name = "ordenanza/ordenanza_create.html"
    success_url = reverse_lazy('ordenanza_list')
    permission_required = 'AppDigestoVillaNueva.add_ordenanza'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        # Obtiene el valor máximo de numero_ordenanza del año actual + 1
        today = date.today()
        year = today.year
        max_ordenanza = Ordenanza.objects.filter(anio=year).aggregate(Max('numero_ordenanza'))['numero_ordenanza__max']

        # Si no hay ningún ordenanza para el año actual, asigna 1 como valor predeterminado
        if max_ordenanza is None:
            max_ordenanza = 1
        else:
            max_ordenanza += 1

        # Devuelve un diccionario con el valor predeterminado para numero_ordenanza
        return {'numero_ordenanza': max_ordenanza}
    
    def form_valid(self, form):
        # Asigna el usuario actual como creador y modificador del ordenanza
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class OrdenanzaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ordenanza
    form_class = OrdenanzaForm
    template_name = "ordenanza/ordenanza_edit.html"
    success_url = reverse_lazy('ordenanza_list')
    permission_required = 'AppDigestoVillaNueva.change_ordenanza'

    def form_valid(self, form):
        # Asigna el usuario actual como modificador del ordenanza
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class OrdenanzaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Ordenanza
    template_name = "ordenanza/ordenanza_list.html"
    context_object_name = 'ordenanza'
    permission_required = 'AppDigestoVillaNueva.view_ordenanza'
    
    def get_queryset(self):
        return Ordenanza.objects.filter(eliminado=False).order_by('-anio', '-numero_ordenanza')

class OrdenanzaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ordenanza
    fields = ['eliminado']
    permission_required = 'AppDigestoVillaNueva.delete_ordenanza'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.eliminado = True
        self.object.save()
        return redirect('ordenanza_list')
    
class OrdenanzaPublicarView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Ordenanza
    fields = ['publicado']
    permission_required = 'AppDigestoVillaNueva.admin_ordenanza'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.publicado = True
        self.object.fecha_publicacion = date.today()
        self.object.save()
        return redirect('ordenanza_list')

class OrdenanzaPublicarMasivoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'AppDigestoVillaNueva.admin_ordenanza'
    def get(self, request):
        return render(request, 'ordenanza/ordenanza_publicacion_masiva.html')

    def post(self, request):
        if 'confirmar' in request.POST:
            # Si se confirma la publicación, publicar los ordenanzas
            ordenanzas_a_publicar_ids = request.session.get('ordenanzas_a_publicar_ids', [])
            ordenanzas_a_publicar = Ordenanza.objects.filter(id__in=ordenanzas_a_publicar_ids)
            for ordenanza in ordenanzas_a_publicar:
                ordenanza.publicado = True
                ordenanza.fecha_publicacion = date.today()
                ordenanza.save()
            del request.session['ordenanzas_a_publicar_ids']  # Limpiar la sesión
            return redirect('ordenanza_list')
        else:
            # Obtener las fechas y filtrar los ordenanzas
            fecha_desde = request.POST.get('fecha_desde')
            fecha_hasta = request.POST.get('fecha_hasta')
            if fecha_desde and fecha_hasta:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                ordenanzas = Ordenanza.objects.filter(fecha_creacion__range=(fecha_desde, fecha_hasta))
                ordenanzas_a_publicar = [ordenanza for ordenanza in ordenanzas if ordenanza.archivo_pdf and not ordenanza.fecha_publicacion]
                # Almacenar los IDs de los ordenanzas a publicar en la sesión
                request.session['ordenanzas_a_publicar_ids'] = [ordenanza.id for ordenanza in ordenanzas_a_publicar]
                return render(request, 'ordenanza/ordenanza_confirmar_publicacion.html', {'ordenanzas': ordenanzas_a_publicar})
            else:
                return redirect('ordenanza_list')


def ordenanza_pdf_view(request, pk):
    ordenanza = get_object_or_404(Ordenanza, pk=pk)
    
    with open(ordenanza.archivo_pdf.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        filename = 'Ordenanza-{0}-{1:04d}.pdf'.format(ordenanza.anio, ordenanza.numero_ordenanza)
        response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
        return response