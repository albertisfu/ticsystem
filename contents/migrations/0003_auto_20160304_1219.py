# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_design_examples'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='design',
            name='content',
        ),
        migrations.AddField(
            model_name='content',
            name='content',
            field=models.OneToOneField(null=True, blank=True, to='contents.Design'),
            preserve_default=True,
        ),
    ]
