from django.db import models

# Create your models here.

class BaseModel(models.Model):
    
    # todo

    id = models.AutoField(primary_key=True)
    state = models.BooleanField('Estado', default = True)
    created_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    deleted_date = models.DateField('Fecha de Eliminacion', auto_now=True, auto_now_add = False)

    #Agregar rent_day

    class Meta: 
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Bases'


    def __str__(self):
        pass