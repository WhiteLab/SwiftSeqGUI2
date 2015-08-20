# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swiftseqgui2', '0002_auto_20150810_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='programmatic_name',
            field=models.CharField(default='default', max_length=1024, verbose_name=b'Programmatic Answer Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='programmatic_name',
            field=models.CharField(default='default', max_length=1024, verbose_name=b'Programmatic Question Name'),
            preserve_default=False,
        ),
    ]
