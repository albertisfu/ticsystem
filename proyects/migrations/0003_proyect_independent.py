# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '0002_remove_proyect_independent'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyect',
            name='independent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
