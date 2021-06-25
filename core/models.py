from django.db import models
from datetime import date
from django.urls import reverse, reverse_lazy

OTRAS_OPTIONES = (
    ('SI', 'si'),
    ('NO', 'no')
)


# Create your models here.
class Pacientes(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    cedula = models.IntegerField(primary_key=True, verbose_name='Cedula')
    phone = models.IntegerField(verbose_name='Telefono')
    nacdate = models.DateField(verbose_name='Fecha de nacimiento')
    image = models.ImageField(upload_to='media', verbose_name='Foto del paciente')
    #labref = models.CharField(max_length=50, blank=True)
    #validacion = models.CharField(max_length=100, blank=True, null=True, verbose_name='Validado por')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    #Redefinir el metodo para calcular la edad exacta tomando meses y dias.
    def calcular_años(self):
        fecha_actual = date.today()
        resultado = fecha_actual.year - self.nacdate.year
        # esta re asicnacion a resultado nos comprueba la edad exacta contando los meses
        resultado -= ((fecha_actual.month, fecha_actual.day) < (self.nacdate.month, self.nacdate.day))
        return resultado


    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return str(self.name)



#se deja como reporte de un cliente en la bases de datos. Falta agregar numero y email
class ExamenesPrice(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del examen")
    precio = models.IntegerField(verbose_name="Precio")

    class Meta:
        verbose_name = "Precio Examene"

    def __str__(self):
        return str(self.name)

#Entrada nueva de examenes
class Entradas(models.Model):
    cedula = models.IntegerField()
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    examenes = models.ForeignKey(ExamenesPrice, on_delete=models.CASCADE)
    #doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Entrada"
        #mordering = ['created']

    def __unicode__(self):
        return str(self.cedula)

class Examenes(models.Model):
    name = models.ForeignKey(Pacientes, on_delete=models.CASCADE, verbose_name='Nombre', default=True)
    exacedula = models.IntegerField(verbose_name="Cedula")
    birth_day = models.DateField(verbose_name='Fecha de nacimiento' )
    ref = models.IntegerField(verbose_name="Referencia del Examen")
    examenes = models.OneToOneField(ExamenesPrice, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Examenes a enviar')
    fiebre = models.CharField(max_length=2, choices=OTRAS_OPTIONES)
    ayuno = models.CharField(max_length=2, choices=OTRAS_OPTIONES)
    diabetes = models.CharField(max_length=2, choices=OTRAS_OPTIONES)
    medicamentos = models.TextField(max_length=250, blank=True, null=True, verbose_name='Medicamentos')
    image = models.ImageField(verbose_name='Imagen del examen')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def años(self):
        fecha_actual = date.today()
        resultado = fecha_actual.year - self.birth_day.year
        # esta re asicnacion a resultado nos comprueba la edad exacta contando los meses
        resultado -= ((fecha_actual.month, fecha_actual.day) < (self.birth_day.month, self.birth_day.day))
        return resultado

    class Meta:
        verbose_name = "Examene"
        ordering = ['created']


    def __str__(self):
        return str(self.name)


#Historias Crud

class Historias(models.Model):
    name = models.ForeignKey(Pacientes, on_delete=models.CASCADE, verbose_name="Nombre")
    identificacion = models.IntegerField(verbose_name='Cedula')
    history = models.TextField(verbose_name='Historia Clinica')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    """def get_absolute_url(self):
        return reverse_lazy('core:hist_detail', args=[self.Historias.object])"""

    """#Guarda el registro con el name en mayusculas
        def save(self):
            self.name = self.name.upper()
            super(Historias, self).save()"""

    class Meta:
        verbose_name = 'Historia clinica'


    def __str__(self):
        return str(self.paciente)







