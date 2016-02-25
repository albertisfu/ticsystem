# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentNuevo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=140)),
                ('object_id', models.PositiveIntegerField()),
                ('mount', models.FloatField()),
                ('method', models.IntegerField(default=1, choices=[(1, b'Deposito'), (2, b'Trasferencia'), (3, b'Tarjeta'), (4, b'Oxxo'), (5, b'Paypal')])),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pendiente'), (2, b'Verificado'), (3, b'Conflicto'), (4, b'Cancelado'), (5, b'Rembolsado')])),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to='customers.Customer', to_field=b'user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
