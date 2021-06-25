from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django.forms import ModelForm
from .models import Pacientes
from .models import Historias as HistoriasModel, Entradas
from .models import Examenes as ExamenesModel



# class DateInput(forms.DateInput)

class PacientForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['name', 'phone', 'nacdate', 'image', 'cedula']
        widgets = {
            'name': forms.TextInput(),
            'phone': forms.NumberInput(),
            'nacdate': forms.NumberInput(attrs={'type': 'date'}),
            #'cedula' : forms.NumberInput(),
            #'image' : forms.ImageField(label='Imagen'),
            # 'id' : forms.IntegerField(label='Cedula', required=True),
        }


class ExamenesForm(forms.ModelForm):
    model = ExamenesModel
    fields = "__all__"

    class Meta:
        model = ExamenesModel
        fields = "__all__"
        widgets = {
            'birth_day': forms.NumberInput(attrs={'type': 'date'}),
        }

class HistoriasForm(forms.ModelForm):
    class Meta:
        model = HistoriasModel
        fields = ['identificacion', 'name', 'history']
        widgets = {
            'history': forms.Textarea(),

        }


class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entradas
        fields = '__all__'