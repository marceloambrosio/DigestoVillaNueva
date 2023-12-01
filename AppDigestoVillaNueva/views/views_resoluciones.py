from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, ListView, View
from django.urls import reverse_lazy
from datetime import date
from django.db.models import Max
from ..models import Resolucion
from ..forms import ResolucionForm
from datetime import datetime

# Create your views here.

class ResolucionCreateView(CreateView):
    model = Resolucion
    form_class = ResolucionForm
    template_name = "resolucion/resolucion_create.html"
    success_url = reverse_lazy('resolucion_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        # Obtiene el valor máximo de resolucion del año actual + 1
        today = date.today()
        year = today.year
        max_resolucion = Resolucion.objects.filter(anio=year).aggregate(Max('numero_resolucion'))['numero_resolucion__max']

        # Si no hay ningún resolucion para el año actual, asigna 1 como valor predeterminado
        if max_resolucion is None:
            max_resolucion = 1
        else:
            max_resolucion += 1

        # Devuelve un diccionario con el valor predeterminado para numero_resolucion
        return {'numero_resolucion': max_resolucion}
    
    def form_valid(self, form):
        # Asigna el usuario actual como creador y modificador del resolucion
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class ResolucionUpdateView(UpdateView):
    model = Resolucion
    form_class = ResolucionForm
    template_name = "resolucion/resolucion_edit.html"
    success_url = reverse_lazy('resolucion_list')

    def form_valid(self, form):
        # Asigna el usuario actual como modificador del resolucion
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class ResolucionListView(ListView):
    model = Resolucion
    template_name = "resolucion/resolucion_list.html"
    context_object_name = 'resoluciones'
    
    def get_queryset(self):
        return Resolucion.objects.filter(eliminado=False).order_by('-anio', '-numero_resolucion')

class ResolucionDeleteView(UpdateView):
    model = Resolucion
    fields = ['eliminado']

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.eliminado = True
        self.object.save()
        return redirect('resolucion_list')
    
class ResolucionPublicarView(UpdateView):
    model = Resolucion
    fields = ['publicado']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.publicado = True
        self.object.fecha_publicacion = date.today()
        self.object.save()
        return redirect('resolucion_list')

class ResolucionPublicarMasivoView(View):
    def get(self, request):
        return render(request, 'resolucion/resolucion_publicacion_masiva.html')

    def post(self, request):
        if 'confirmar' in request.POST:
            # Si se confirma la publicación, publicar los resoluciones
            resoluciones_a_publicar_ids = request.session.get('resoluciones_a_publicar_ids', [])
            resoluciones_a_publicar = Resolucion.objects.filter(id__in=resoluciones_a_publicar_ids)
            for resolucion in resoluciones_a_publicar:
                resolucion.publicado = True
                resolucion.fecha_publicacion = date.today()
                resolucion.save()
            del request.session['resoluciones_a_publicar_ids']  # Limpiar la sesión
            return redirect('resolucion_list')
        else:
            # Obtener las fechas y filtrar los resoluciones
            fecha_desde = request.POST.get('fecha_desde')
            fecha_hasta = request.POST.get('fecha_hasta')
            if fecha_desde and fecha_hasta:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                resoluciones = Resolucion.objects.filter(fecha_creacion__range=(fecha_desde, fecha_hasta))
                resoluciones_a_publicar = [resolucion for resolucion in resoluciones if resolucion.archivo_pdf and not resolucion.fecha_publicacion]
                # Almacenar los IDs de los resoluciones a publicar en la sesión
                request.session['resoluciones_a_publicar_ids'] = [resolucion.id for resolucion in resoluciones_a_publicar]
                return render(request, 'resolucion/resolucion_confirmar_publicacion.html', {'resoluciones': resoluciones_a_publicar})
            else:
                return redirect('resolucion_list')


def resolucion_pdf_view(request, pk):
    resolucion = get_object_or_404(Resolucion, pk=pk)
    
    with open(resolucion.archivo_pdf.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        filename = 'Resolucion-{0}-{1:04d}.pdf'.format(resolucion.anio, resolucion.numero_resolucion)
        response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
        return response