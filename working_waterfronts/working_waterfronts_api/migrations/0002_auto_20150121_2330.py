# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('working_waterfronts_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='pointofinterest',
        ),
        migrations.RemoveField(
            model_name='video',
            name='pointofinterest',
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='images',
            field=models.ManyToManyField(to='working_waterfronts_api.Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='videos',
            field=models.ManyToManyField(to='working_waterfronts_api.Video', blank=True),
            preserve_default=True,
        ),
    ]
