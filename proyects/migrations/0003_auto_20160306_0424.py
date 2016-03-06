# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '0002_auto_20160301_0746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyect',
            name='activation',
        ),
        migrations.AddField(
            model_name='package',
            name='activation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
