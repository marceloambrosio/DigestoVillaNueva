from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import date
from django.db.models import Max
from ..models import Declaracion
from ..forms import DeclaracionForm
from datetime import datetime

# Create your views here.

class DeclaracionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Declaracion
    form_class = DeclaracionForm
    template_name = "declaracion/declaracion_create.html"
    success_url = reverse_lazy('declaracion_list')
    permission_required = 'AppDigestoVillaNueva.add_declaracion'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        # Obtiene el valor máximo de numero_declaracion del año actual + 1
        today = date.today()
        year = today.year
        max_declaracion = Declaracion.objects.filter(anio=year).aggregate(Max('numero_declaracion'))['numero_declaracion__max']

        # Si no hay ningún declaracion para el año actual, asigna 1 como valor predeterminado
        if max_declaracion is None:
            max_declaracion = 1
        else:
            max_declaracion += 1

        # Devuelve un diccionario con el valor predeterminado para numero_declaracion
        return {'numero_declaracion': max_declaracion}
    
    def form_valid(self, form):
        # Asigna el usuario actual como creador y modificador del declaracion
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class DeclaracionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Declaracion
    form_class = DeclaracionForm
    template_name = "declaracion/declaracion_edit.html"
    success_url = reverse_lazy('declaracion_list')
    permission_required = 'AppDigestoVillaNueva.change_declaracion'

    def form_valid(self, form):
        # Asigna el usuario actual como modificador del declaracion
        form.instance.modificado_por = self.request.user

        # Obtén la fecha de publicación del formulario
        fecha_publicacion = form.cleaned_data.get('fecha_publicacion')

        # Si hay una fecha de publicación, establece publicado en True
        if fecha_publicacion:
            form.instance.publicado = True

        # Llama al método form_valid de la clase base para continuar con el procesamiento estándar
        return super().form_valid(form)

class DeclaracionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Declaracion
    template_name = "declaracion/declaracion_list.html"
    context_object_name = 'declaraciones'
    permission_required = 'AppDigestoVillaNueva.view_declaracion'
    
    def get_queryset(self):
        return Declaracion.objects.filter(eliminado=False).order_by('-anio', '-numero_declaracion')

class DeclaracionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Declaracion
    fields = ['eliminado']
    permission_required = 'AppDigestoVillaNueva.delete_declaracion'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.eliminado = True
        self.object.save()
        return redirect('declaracion_list')
    
class DeclaracionPublicarView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Declaracion
    fields = ['publicado']
    permission_required = 'AppDigestoVillaNueva.admin_declaracion'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.publicado = True
        self.object.fecha_publicacion = date.today()
        self.object.save()
        return redirect('declaracion_list')

class DeclaracionPublicarMasivoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'AppDigestoVillaNueva.admin_declaracion'
    def get(self, request):
        return render(request, 'declaracion/declaracion_publicacion_masiva.html')

    def post(self, request):
        if 'confirmar' in request.POST:
            # Si se confirma la publicación, publicar los declaraciones
            declaraciones_a_publicar_ids = request.session.get('declaraciones_a_publicar_ids', [])
            declaraciones_a_publicar = Declaracion.objects.filter(id__in=declaraciones_a_publicar_ids)
            for declaracion in declaraciones_a_publicar:
                declaracion.publicado = True
                declaracion.fecha_publicacion = date.today()
                declaracion.save()
            del request.session['declaraciones_a_publicar_ids']  # Limpiar la sesión
            return redirect('declaracion_list')
        else:
            # Obtener las fechas y filtrar los declaracion
            fecha_desde = request.POST.get('fecha_desde')
            fecha_hasta = request.POST.get('fecha_hasta')
            if fecha_desde and fecha_hasta:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                declaraciones = Declaracion.objects.filter(fecha_creacion__range=(fecha_desde, fecha_hasta))
                declaraciones_a_publicar = [declaracion for declaracion in declaraciones if declaracion.archivo_pdf and not declaracion.fecha_publicacion]
                # Almacenar los IDs de los declaraciones a publicar en la sesión
                request.session['declaraciones_a_publicar_ids'] = [declaracion.id for declaracion in declaraciones_a_publicar]
                return render(request, 'declaracion/declaracion_confirmar_publicacion.html', {'declaraciones': declaraciones_a_publicar})
            else:
                return redirect('declaracion_list')


def declaracion_pdf_view(request, pk):
    declaracion = get_object_or_404(Declaracion, pk=pk)
    
    with open(declaracion.archivo_pdf.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        filename = 'Declaracion-{0}-{1:04d}.pdf'.format(declaracion.anio, declaracion.numero_declaracion)
        response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
        return response