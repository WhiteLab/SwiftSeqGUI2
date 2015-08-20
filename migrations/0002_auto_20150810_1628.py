# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swiftseqgui2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='multiple_programs',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
