from django.urls import path
from .reportes import reporte_examenes, imprimir_examen

reportes_patterns =([
     # para reportes examenes
    path('reportes/listado/print', reporte_examenes, name='examenes_print_all'),
    path('reportes/<int:examen_id>/imprimir', imprimir_examen, name="examen_print_one"),

], 'reportes')