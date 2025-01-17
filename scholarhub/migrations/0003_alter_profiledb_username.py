# Generated by Django 5.0 on 2024-06-27 04:51

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarhub', '0002_profiledb_otp_profiledb_otp_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledb',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
