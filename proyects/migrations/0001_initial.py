# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('price', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('totalprice', models.FloatField(null=True, blank=True)),
                ('featureds', models.ManyToManyField(to='proyects.Featured')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=140)),
                ('progress', models.PositiveIntegerField(null=True, blank=True)),
                ('independent', models.BooleanField(default=False)),
                ('mount', models.FloatField(null=True, blank=True)),
                ('deposit', models.IntegerField(default=35)),
                ('advancepayment', models.FloatField(null=True, blank=True)),
                ('remaingpayment', models.FloatField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pendiente'), (2, b'Proceso'), (3, b'Terminado'), (4, b'Cancelado')])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(to='proyects.Package')),
                ('user', models.ForeignKey(to='customers.Customer', to_field=b'user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
