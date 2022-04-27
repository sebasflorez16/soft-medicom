import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.utils import timezone

from core.models import Examenes as Examenesmodel


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

# imprimir todas las entradas de examenes
def reporte_examenes(request):
    template_path = 'reportes/examenes_print_all.html'
    today = timezone.now()

    examenes = Examenesmodel.objects.all()
    context = {
        'obj': examenes,
        'today': today,
        'request': request
    }
    response = HttpResponse(content_type='aplication/pdf')
    response['content-Disposition'] = 'attachment; filename="todos_los examenes.pdf' #nombre del pdf generado
    template = get_template(template_path)
    html = template.render(context)

    #crear el pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#impresion para un solo examen
def imprimir_examen(request, examen_id):
    template_path = 'reportes/examenes_print_one.html'
    today = timezone.now()

    examen = Examenesmodel.objects.filter(id=examen_id).first()
    if examen:
        detalle = Examenesmodel.objects.filter(id=examen_id)
    else:
        detalle={}

    context = {

        'detalle': detalle,
        #'examen': examen,
        'today': today,
        'request': request
    }

    response = HttpResponse(content_type='aplication/pdf')
    response['content-Disposition'] = 'inline; filename="examen_personal.pdf'  # nombre del pdf generado
    template = get_template(template_path)
    html = template.render(context)

    # crear el pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




