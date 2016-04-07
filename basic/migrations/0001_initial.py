# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=10)),
                ('friends', models.ManyToManyField(to='basic.UserProfile', through='basic.Friendship')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(related_name='friend', to='basic.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='person',
            field=models.ForeignKey(to='basic.UserProfile'),
        ),
    ]
