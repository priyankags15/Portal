# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_count', models.IntegerField(default=0)),
                ('candidature_date', models.DateField()),
                ('agenda', models.TextField(max_length=500, blank=True)),
                ('candidate_designation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Citizens',
            fields=[
                ('user_name', models.IntegerField(serialize=False, primary_key=True)),
                ('First_name', models.TextField()),
                ('Last_name', models.TextField()),
                ('Address', models.TextField()),
                ('email', models.EmailField(max_length=200)),
                ('contact', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Election_duration',
            fields=[
                ('election_year', models.IntegerField(serialize=False, primary_key=True)),
                ('polling_date', models.DateField()),
                ('candidature_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Login_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name=b'Citizens')),
                ('password', models.TextField()),
                ('designation', models.TextField()),
                ('user_name', models.ForeignKey(to='Election.Citizens')),
            ],
        ),
        migrations.CreateModel(
            name='Vote_Casted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('casted_year', models.DateField()),
                ('user_name', models.ForeignKey(to='Election.Citizens')),
            ],
        ),
        migrations.AddField(
            model_name='candidates',
            name='user_name',
            field=models.ForeignKey(to='Election.Citizens'),
        ),
    ]
