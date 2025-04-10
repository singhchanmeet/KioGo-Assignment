# Generated by Django 5.0 on 2025-04-01 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedDomains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('one_time_password', models.CharField(max_length=100)),
                ('pasword_expiry_time', models.DateTimeField(default=datetime.datetime(2025, 4, 1, 12, 34, 16, 915720, tzinfo=datetime.timezone.utc))),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
