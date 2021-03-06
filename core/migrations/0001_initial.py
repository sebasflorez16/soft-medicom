# Generated by Django 3.0 on 2022-03-23 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamenesPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del examen')),
                ('precio', models.IntegerField(verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Precio Examene',
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('cedula', models.IntegerField(primary_key=True, serialize=False, verbose_name='Cedula')),
                ('phone', models.IntegerField(verbose_name='Telefono')),
                ('nacdate', models.DateField(verbose_name='Fecha de nacimiento')),
                ('image', models.ImageField(upload_to='media', verbose_name='Foto del paciente')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Historias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.IntegerField(verbose_name='Cedula')),
                ('history', models.TextField(verbose_name='Historia Clinica')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pacientes', verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Historia clinica',
            },
        ),
        migrations.CreateModel(
            name='Examenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exacedula', models.IntegerField(verbose_name='Cedula')),
                ('birth_day', models.DateField(verbose_name='Fecha de nacimiento')),
                ('ref', models.IntegerField(verbose_name='Referencia del Examen')),
                ('fiebre', models.CharField(choices=[('SI', 'si'), ('NO', 'no')], max_length=2)),
                ('ayuno', models.CharField(choices=[('SI', 'si'), ('NO', 'no')], max_length=2)),
                ('diabetes', models.CharField(choices=[('SI', 'si'), ('NO', 'no')], max_length=2)),
                ('medicamentos', models.TextField(blank=True, max_length=250, null=True, verbose_name='Medicamentos')),
                ('image', models.ImageField(upload_to='', verbose_name='Imagen del examen')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('examenes', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ExamenesPrice', verbose_name='Examenes a enviar')),
                ('name', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='core.Pacientes', verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Examene',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Entradas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('examenes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ExamenesPrice')),
            ],
            options={
                'verbose_name': 'Entrada',
            },
        ),
    ]
