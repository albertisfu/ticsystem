# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostingservice',
            name='domain',
            field=models.CharField(max_length=600, null=True, blank=True),
            preserve_default=True,
        ),
    ]
