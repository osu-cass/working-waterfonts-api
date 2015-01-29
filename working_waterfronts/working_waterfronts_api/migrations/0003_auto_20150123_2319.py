# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('working_waterfronts_api', '0002_auto_20150121_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='pointofinterests',
            field=models.ManyToManyField(
                to='working_waterfronts_api.PointOfInterest', null=True, blank=True),
            preserve_default=True,
        ),
    ]
