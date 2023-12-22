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
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import gray

def generar_portada(boletin_id):
    # Obtén el boletín
    boletin = BoletinOficial.objects.get(id=boletin_id)

    # Crea un nuevo objeto Canvas con tamaño de hoja A4
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Define la fuente y el tamaño de la fuente
    c.setFont("Helvetica-Bold", 30)

    # Dibuja el título centrado y más abajo
    c.drawCentredString(A4[0] / 2, 650, "Boletín Oficial")

    # Cambia el tamaño de la fuente para la fecha
    c.setFont("Helvetica", 18)

    # Cambia el color de la fuente a gris
    c.setFillColor(gray)

    # Dibuja la fecha centrada y más abajo
    c.drawCentredString(A4[0] / 2, 610, boletin.fecha_creacion.strftime('%d/%m/%Y'))

    # Carga la imagen de la portada
    portada = Image('img/boletinoficial/boletin_portada.png')

    # Ajusta el tamaño de la imagen para que ocupe todo el ancho de la hoja
    portada_width = A4[0]
    portada_height = portada.drawHeight * portada_width / portada.drawWidth
    portada = Image('img/boletinoficial/boletin_portada.png', width=portada_width, height=portada_height)

    # Dibuja la imagen de portada centrada y abajo
    portada.drawOn(c, (A4[0] - portada.drawWidth) / 2, 300)

    # Carga el nuevo logo
    logo = Image('img/boletinoficial/boletin_pie.png')

    # Ajusta el tamaño del logo para que tenga un alto de 50 y mantenga su relación de aspecto original
    logo_height = 80
    logo_width = logo.drawWidth * logo_height / logo.drawHeight
    logo = Image('img/boletinoficial/boletin_pie.png', width=logo_width, height=logo_height)

    # Calcula la posición x para centrar el logo
    logo_x = (A4[0] - logo_width) / 2

    # Dibuja el logo en el pie de la página
    logo.drawOn(c, logo_x, 50)

    # Guarda el PDF
    c.showPage()
    c.save()

    # Devuelve el PDF como un objeto de bytes
    buffer.seek(0)
    return buffer.read()

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
    portada = generar_portada(boletin.id)

    # Crea un objeto PdfMerger
    merger = PdfMerger()

    # Añade la portada al PDF
    merger.append(BytesIO(portada))

    # Añade los documentos al PDF
    for documento in documentos:
        merger.append(documento.archivo_pdf.path)

    # Crea un objeto BytesIO para guardar el PDF
    pdf_buffer = BytesIO()

    # Escribe el PDF en el buffer
    merger.write(pdf_buffer)

    # Cierra el objeto PdfMerger
    merger.close()

    # Almacena el PDF en el campo archivo_pdf
    pdf_buffer.seek(0)
    boletin.archivo_pdf.save('Boletin-{0}.pdf'.format(boletin.fecha_creacion), ContentFile(pdf_buffer.read()))

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