# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0006_auto_20160305_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='example',
            field=models.OneToOneField(null=True, blank=True, to='contents.Examples'),
            preserve_default=True,
        ),
    ]
