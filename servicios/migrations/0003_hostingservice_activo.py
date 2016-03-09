# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_hostingservice_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostingservice',
            name='activo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
