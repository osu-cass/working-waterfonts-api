# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.TextField(default=b'')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images')),
                ('name', models.TextField(default=b'')),
                ('caption', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PointOfInterest',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('alt_name', models.TextField(blank=True)),
                ('description', models.TextField()),
                ('history', models.TextField()),
                ('facts', models.TextField()),
                ('location', django.contrib.gis.db.models.fields.PointField(
                    srid=4326)),
                ('street', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('location_description', models.TextField(blank=True)),
                ('zip', models.TextField()),
                ('contact_name', models.TextField()),
                ('website', models.URLField(blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(
                    max_length=128, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(
                    to='working_waterfronts_api.Category', blank=True)),
                ('hazards', models.ManyToManyField(
                    to='working_waterfronts_api.Hazard', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.URLField()),
                ('caption', models.TextField(blank=True)),
                ('name', models.TextField(default=b'')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('pointofinterest', models.ForeignKey(
                    to='working_waterfronts_api.PointOfInterest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='image',
            name='pointofinterest',
            field=models.ForeignKey(
                to='working_waterfronts_api.PointOfInterest'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='pointofinterests',
            field=models.ManyToManyField(
                to='working_waterfronts_api.PointOfInterest'),
            preserve_default=True,
        ),
    ]
