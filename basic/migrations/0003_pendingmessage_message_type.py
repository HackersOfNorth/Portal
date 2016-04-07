# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20160403_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingmessage',
            name='message_type',
            field=models.CharField(default='1', max_length=100),
            preserve_default=False,
        ),
    ]
