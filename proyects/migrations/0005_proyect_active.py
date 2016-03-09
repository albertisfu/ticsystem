# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '0004_package_hosting'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyect',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
