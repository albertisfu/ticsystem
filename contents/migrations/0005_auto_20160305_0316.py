# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0004_design_package'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='content',
            new_name='design',
        ),
    ]
