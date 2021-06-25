from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .forms import PacientForm, HistoriasForm, ExamenesForm, EntradasForm
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.views.generic.base import TemplateView
from .models import Pacientes
from .models import Historias as HistoriasModel, Entradas
from .models import Examenes as ExamenesModel, ExamenesPrice
from django.views.generic.list import ListView



# Create your views here.


class DashView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = "core/dash.html"


@login_required(login_url='login/')
def home(request):
    form = PacientForm
    if request.method == 'POST':
        form = PacientForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect(reverse('core:home') + '?ok')

        def id_count(request):
            q = Pacientes.objects.GET(Count('id'))
            if Pacientes.not_exist():
                q = Pacientes.id + 1

    return render(request, 'core/home.html', {'form': form})


class EntradasNew(FormView):
    model = Entradas
    form_class = EntradasForm
    template_name = 'core/entradas.html'
    success_url = reverse_lazy('core:dash')

    def form_valid(self, form):
        if self.name.exists(Pacientes):
            name.get()
        else:
            Pacientes.create()
        form.save()
        return super(EntradasNew, self).form_valid(form)

    def get_object(self):
        paciente, create = Pacientes.objects.get_or_create(Pacientes=self.name)
        return paciente

class ListPacientes(LoginRequiredMixin, ListView):
    login_url = 'login/'
    model = Pacientes
    template_name = 'pacientes_list.html'


class PacienteDetail(DetailView):
    model = Pacientes
    template_name = 'core/paciente_detail.html'

    def get_context_data(self, *args, **kwargs): #busca e imprime todos los datos sin filtrar
        context = super().get_context_data(*args, **kwargs)
        # context['now'] = timezone.now()
        return context


class PacienteUpdate(LoginRequiredMixin, UpdateView):
    model = Pacientes
    form = PacientForm
    fields = ['name', 'phone', 'nacdate', 'image', 'cedula']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('detail', args=[self.object.id])


class PacienteDelete(LoginRequiredMixin, DeleteView):
    model = Pacientes
    success_message = "El paciente ha diso eliminado de la base de datos"

    def get_success_url(self):
        return reverse_lazy('core:lista') + '?ok'



#Examenes CRUD


"""def examenes_add(request):
    form = ExamenesForm
    if request == 'POST':
        form = ExamenesForm
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect(reverse('core:lista'))

    return render(request, 'core/examenes.html', {'form':form})"""



class Examenes(FormView):
    form_class = ExamenesForm
    model = ExamenesModel
    template_name = 'core/examenes.html'
    succes_message = 'El registro ha sido creado'
    #success_url = reverse_lazy('core:examenes_list')

    def form_valid(self, form):
        form.save()
        return super(Examenes, self).form_valid(form)
        
    def get_success_url(self):
        #podriamos dar mas personalizacion usando el messagemixin para usar fields del modelo como el nombre
        messages.success(self.request, 'Haz agregado el examen con exito')
        return reverse('core:lista')


class Exam_suc(TemplateView):
    model = ExamenesModel
    template_name = 'core/examenes_confirm_delete.html'

class ListExamenes(LoginRequiredMixin, ListView):
    login_url = 'core:login/'
    model = ExamenesModel
    fields = ['name', 'ref']
    template_name = 'core/examenes_list.html'

    def get_queryset(self, **kwargs):
        return ExamenesModel.objects.filter(name=self.kwargs['pk'])


class ExamenDetail(LoginRequiredMixin, ListView):
    login_url = 'core:login/'
    model = ExamenesModel
    template_name = 'core/examen_detail.html'

    def get_context_data(self, **kwargs): #busca e imprime todos los datos sin filtrar
        context = super().get_context_data(**kwargs)
        context['price'] = ExamenesPrice.objects.all()
        return context


class PriceDetail(ListView):
    model = ExamenesPrice


"""    def get_queryset(self):
        return Pacientes.objects.filter(name_id=self.kwargs['pk'])"""

class ExamenesDelete(DeleteView):
    model = ExamenesModel
    success_url = reverse_lazy('core:examen_delete')

    """def get_success_url(self):
        return reverse_lazy('core:examenes_list', kwargs={'pk': self.kwargs['pk']})"""

class ExamanSuccesfull(TemplateView):
    model = Pacientes
    template_name = 'core/exam_succesfull.html'

    def get_success_url(self):
        return reverse_lazy('core:examenes_list', kwargs={'id':self.examenes_id})





# historias CRUD
class Historia_Add_View(SuccessMessageMixin, CreateView):
    form_class = HistoriasForm
    model = HistoriasModel
    template_name = 'core/historia_add.html'
    #success_url = reverse_lazy('core:lista')
    success_message = "Se ha registrado la historiria clinica con exito. "

    def get_success_url(self):
        return reverse_lazy('core:hist_detail', args=(self.object.id,)) #Se debe pasar la coma al final por que si no se interpretaria como un obj iterable


class HistoriasList(ListView):
    model = HistoriasModel
    #queryset = HistoriasModel.object.filter(HistoriasModel=Pacientes.pk)
    fields = ['name', 'history']
    template_name = 'core/historiaslist_list.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        return HistoriasModel.objects.filter(identificacion=self.kwargs['pk']).order_by('created')



class HistoriasDetail(DetailView):
    model = HistoriasModel
    template_name = 'core/historias_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class HistoriasDelete(DeleteView):
    model = HistoriasModel
    success_message = "El registro ha diso eliminado de la base de datos"
    success_url = reverse_lazy('core:historias_list')
    success_message = "El registro ha sido borrado de la lista de Historias clinicas"

    """def get_success_url(self):
        return reverse_lazy('core:historias_list', args=[self.object.id])"""