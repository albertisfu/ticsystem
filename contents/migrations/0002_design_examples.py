# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to=b'static/files')),
                ('description', models.CharField(max_length=2000)),
                ('content', models.OneToOneField(to='contents.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Examples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to=b'static/files')),
                ('url', models.CharField(max_length=250, null=True, blank=True)),
                ('description', models.CharField(max_length=2000)),
                ('content', models.ForeignKey(to='contents.Design')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
