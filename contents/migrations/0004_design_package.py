# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '0002_auto_20160301_0746'),
        ('contents', '0003_auto_20160304_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='package',
            field=models.ForeignKey(blank=True, to='proyects.Package', null=True),
            preserve_default=True,
        ),
    ]
