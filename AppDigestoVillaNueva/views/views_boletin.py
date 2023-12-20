from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Decreto, Ordenanza, Resolucion, Declaracion, BoletinOficial
from ..forms import BoletinOficialForm
from io import BytesIO
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

def generar_boletin(boletin):
    # Recoge los documentos relevantes
    documentos = []
    if boletin.ordenanzas:
        documentos.extend(Ordenanza.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_ordenanza'))
    if boletin.resoluciones:
        documentos.extend(Resolucion.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_resolucion'))
    if boletin.decretos:
        documentos.extend(Decreto.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_decreto'))
    if boletin.declaraciones:
        documentos.extend(Declaracion.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_declaracion'))

    # Crea la portada del boletín
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, "Boletin Oficial {}".format(boletin.fecha_creacion))
    p.showPage()
    p.save()
    portada = buffer.getvalue()

    # Une los archivos PDF
    merger = PdfMerger()
    merger.append(ContentFile(portada))
    for documento in documentos:
        merger.append(documento.archivo_pdf.path)
    buffer = BytesIO()
    merger.write(buffer)
    merger.close()

    # Almacena el PDF en el campo archivo_pdf
    pdf = buffer.getvalue()
    boletin.archivo_pdf.save('Boletin-{0}.pdf'.format(boletin.fecha_creacion), ContentFile(pdf))
    boletin.save()

@login_required
@permission_required('AppDigestoVillaNueva.add_boletinoficial')
def crear_boletin(request):
    if request.method == 'POST':
        form = BoletinOficialForm(request.POST)
        if form.is_valid():
            boletin = form.save()
            generar_boletin(boletin)  # Llama a la función que genera el PDF
            return redirect('boletinoficial_detail', pk=boletin.pk)
    else:
        form = BoletinOficialForm()
    return render(request, 'boletinoficial/boletin_crear.html', {'form': form})

def boletin_detail(request, pk):
    boletin = get_object_or_404(BoletinOficial, pk=pk)
    documentos = []
    if boletin.ordenanzas:
        documentos.extend(Ordenanza.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_ordenanza'))
    if boletin.resoluciones:
        documentos.extend(Resolucion.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_resolucion'))
    if boletin.decretos:
        documentos.extend(Decreto.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_decreto'))
    if boletin.declaraciones:
        documentos.extend(Declaracion.objects.filter(fecha_creacion__range=[boletin.fecha_desde, boletin.fecha_hasta], publicado=True).order_by('numero_declaracion'))
    return render(request, 'boletinoficial/boletin_detail.html', {'boletin': boletin, 'documentos': documentos})

class BoletinOficialListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BoletinOficial
    template_name = "boletinoficial/boletin_list.html"
    context_object_name = 'boletinoficial'
    permission_required = 'AppDigestoVillaNueva.view_boletinoficial'
    
    def get_queryset(self):
        return BoletinOficial.objects.order_by('-fecha_creacion')
    
def boletin_pdf_view(request, pk):
    boletin = get_object_or_404(BoletinOficial, pk=pk)
    
    with open(boletin.archivo_pdf.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        filename = 'BoletinOficial-{0}.pdf'.format(boletin.fecha_creacion)
        response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
        return response
    
class BoletinOficialDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BoletinOficial
    #template_name = "boletinoficial/boletin_delete.html"
    success_url = reverse_lazy('boletinoficial_list')
    permission_required = 'AppDigestoVillaNueva.delete_boletinoficial'
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.archivo_pdf.delete()
        self.object.delete()
        return redirect(self.success_url)
    
class BoletinOficialPublicarView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BoletinOficial
    fields = ['publicado']
    permission_required = 'AppDigestoVillaNueva.admin_declaracion'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.publicado = True
        self.object.save()
        return redirect('boletinoficial_list')