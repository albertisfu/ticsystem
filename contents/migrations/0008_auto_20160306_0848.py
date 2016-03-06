# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0007_content_example'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='design',
            field=models.ForeignKey(blank=True, to='contents.Design', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='example',
            field=models.ForeignKey(blank=True, to='contents.Examples', null=True),
            preserve_default=True,
        ),
    ]
