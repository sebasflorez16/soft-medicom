from django.contrib import admin

# Register your models here.
from .models import Pacientes, Historias, Examenes, ExamenesPrice, Entradas
from .forms import PacientForm



# Register your models here.

class PacientesAdmin(admin.ModelAdmin):
    form = PacientForm
    list_display = ('name', 'phone', 'nacdate', 'cedula', 'image')
    list_filter = ('cedula',)
    date_hierarchy = 'created'


class ExamenesAdmin(admin.ModelAdmin):
    model = Examenes
    list_display = ('ayuno', 'fiebre', 'diabetes', 'ref', 'examenes', 'exacedula', 'birth_day')

class HistoriasAdmin(admin.ModelAdmin):
    model = Historias
    list_display = ('name', 'identificacion', 'created')

class ExamenesPriceAdmin(admin.ModelAdmin):
    model = ExamenesPrice
    list_display = ('name', 'precio')

class EntradasAdmin(admin.ModelAdmin):
    model = Entradas
    list_display = ('cedula', 'name', 'phone', 'email', 'address')

admin.site.register(Historias, HistoriasAdmin)
admin.site.register(Examenes, ExamenesAdmin)
admin.site.register(ExamenesPrice, ExamenesPriceAdmin)
admin.site.register(Pacientes, PacientesAdmin)
admin.site.register(Entradas, EntradasAdmin)