# Generated by Django 3.1.1 on 2021-11-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0008_auto_20211031_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='member',
            name='sex',
            field=models.CharField(default='', max_length=10),
        ),
    ]
