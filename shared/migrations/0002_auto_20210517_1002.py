# Generated by Django 3.0 on 2021-05-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='on_trial',
            field=models.BooleanField(default=True),
        ),
    ]