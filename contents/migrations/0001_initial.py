# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '__first__'),
        ('fileupload', '0002_auto_20160213_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('empresa', models.CharField(max_length=250)),
                ('giro', models.CharField(max_length=2000)),
                ('numbersections', models.CharField(max_length=1000)),
                ('proyect', models.ForeignKey(to='proyects.Proyect')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilesUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.ForeignKey(to='fileupload.Picture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogoUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.ForeignKey(to='fileupload.Picture')),
                ('content', models.ForeignKey(to='contents.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('coment', models.TextField(max_length=255, null=True, blank=True)),
                ('content', models.ForeignKey(to='contents.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filesupload',
            name='section',
            field=models.ForeignKey(to='contents.Section'),
            preserve_default=True,
        ),
    ]
