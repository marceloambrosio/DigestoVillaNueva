from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
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

def crear_boletin(request):
    if request.method == 'POST':
        form = BoletinOficialForm(request.POST)
        if form.is_valid():
            boletin = form.save()
            generar_boletin(boletin)  # Llama a la función que genera el PDF
            return redirect('boletin_detail', pk=boletin.pk)
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
