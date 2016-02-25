# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('movil', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('proyect', models.ForeignKey(to='proyects.Proyect')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
