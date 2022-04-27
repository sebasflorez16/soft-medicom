from django.urls import path
from . import views
from .views import ListPacientes, PacienteDetail, PacienteUpdate,\
    PacienteDelete, HistoriasList, HistoriasDetail, DashView, ListExamenes, Historia_Add_View, ExamenDetail, \
    HistoriasDelete, ExamenesDelete, ExamanSuccesfull, Examenes, EntradasNew



core_patterns=([
    #rutas para PACIENTES CRUD
    path('', DashView.as_view(), name='dash'),
    path('home/', views.home, name='home'),
    path('entradas_new/', EntradasNew.as_view(), name='entradas_new'),
    path('pacientes_list/', ListPacientes.as_view(), name='lista'),
    path('paciente/<slug:pk>/', PacienteDetail.as_view(), name='detail'),
    path('paciente/update/<slug:pk>/', PacienteUpdate.as_view(), name='update'),
    path('paciente/delete/<slug:pk>/', PacienteDelete.as_view(), name='delete'),

    #ruta para EXAMENES
    path('examenes/new', Examenes.as_view(), name='examenes'),#formulario de nuev examen
    path('examenes/lista/<int:pk>/', ListExamenes.as_view(), name='examenes_list'),
    path('examenes/detail/<slug:pk>/', ExamenDetail.as_view(), name='examen_detail'),
    path('examenes/delete/<slug:pk>/', ExamenesDelete.as_view(), name='examen_delete'),
    path('examenes/examenes/examen_succes/', ExamanSuccesfull.as_view(), name='exam_succesfull'),

    #ruta para HISTORIAS
    path('paciente/historia_add/new', Historia_Add_View.as_view(), name='historia_new'),#se agrega la ultima palabra new por que de resto	ValueError por que esperaba un int y llego historia__add como str
    path('paciente/historias_list/<int:pk>/', HistoriasList.as_view(), name='historias_list'),
    path('paciente/historias_delete/delete/<slug:pk>/', HistoriasDelete.as_view(), name='historia_delete'),
    path('historias_detail/<slug:pk>/', HistoriasDetail.as_view(), name='hist_detail'),


    #ru

], 'core')
