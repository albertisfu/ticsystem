# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0005_auto_20160305_0316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examples',
            old_name='content',
            new_name='design',
        ),
    ]
