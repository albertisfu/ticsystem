# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tdl', models.CharField(max_length=255)),
                ('anualprice', models.FloatField(null=True, blank=True)),
                ('bianualprice', models.FloatField(null=True, blank=True)),
                ('trianualprice', models.FloatField(null=True, blank=True)),
                ('quadanualprice', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('billingcycle', models.IntegerField(default=1, choices=[(1, b'1 a\xc3\xb1o'), (2, b'2 a\xc3\xb1os'), (3, b'3 a\xc3\xb1os'), (4, b'4 a\xc3\xb1os')])),
                ('cycleprice', models.FloatField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pendiente'), (2, b'Activo'), (3, b'Terminado'), (4, b'Conflicto')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_renew', models.DateTimeField(null=True, blank=True)),
                ('next_renew', models.DateTimeField(null=True, blank=True)),
                ('days_left', models.IntegerField(null=True, blank=True)),
                ('dns1', models.CharField(max_length=450, null=True, blank=True)),
                ('dns2', models.CharField(max_length=450, null=True, blank=True)),
                ('domain', models.ForeignKey(to='servicios.Domain')),
                ('user', models.ForeignKey(to='customers.Customer', to_field=b'user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HostingPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('trimestralprice', models.FloatField(null=True, blank=True)),
                ('semestralprice', models.FloatField(null=True, blank=True)),
                ('anualprice', models.FloatField(null=True, blank=True)),
                ('bianualprice', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HostingService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('billingcycle', models.IntegerField(default=3, choices=[(1, b'Trimestral'), (2, b'Semestral'), (3, b'Anual'), (4, b'Bianual')])),
                ('cycleprice', models.FloatField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pendiente'), (2, b'Activo'), (3, b'Terminado'), (4, b'Conflicto')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_renew', models.DateTimeField(null=True, blank=True)),
                ('next_renew', models.DateTimeField(null=True, blank=True)),
                ('days_left', models.IntegerField(null=True, blank=True)),
                ('hosting_panel', models.CharField(max_length=600, null=True, blank=True)),
                ('hosting_password', encrypted_fields.fields.EncryptedCharField(max_length=10, null=True, blank=True)),
                ('webmail', models.CharField(max_length=600, null=True, blank=True)),
                ('ftp_server', models.CharField(max_length=600, null=True, blank=True)),
                ('ftp_port', models.CharField(max_length=600, null=True, blank=True)),
                ('ftp_password', encrypted_fields.fields.EncryptedCharField(max_length=10, null=True, blank=True)),
                ('hostingpackage', models.ForeignKey(to='servicios.HostingPackage')),
                ('user', models.ForeignKey(to='customers.Customer', to_field=b'user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
