# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_hostingservice_domain'),
        ('proyects', '0003_auto_20160306_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='hosting',
            field=models.ForeignKey(blank=True, to='servicios.HostingPackage', null=True),
            preserve_default=True,
        ),
    ]
