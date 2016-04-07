# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagePool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=100)),
                ('source', models.ForeignKey(to='basic.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='messagepool',
            name='message',
            field=models.ForeignKey(to='basic.PendingMessage'),
        ),
        migrations.AddField(
            model_name='messagepool',
            name='person',
            field=models.ForeignKey(to='basic.UserProfile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pending_messages',
            field=models.ManyToManyField(to='basic.PendingMessage', through='basic.MessagePool'),
        ),
    ]
