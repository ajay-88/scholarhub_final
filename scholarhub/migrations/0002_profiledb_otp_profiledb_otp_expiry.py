# Generated by Django 5.0 on 2024-06-18 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarhub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledb',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='profiledb',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]