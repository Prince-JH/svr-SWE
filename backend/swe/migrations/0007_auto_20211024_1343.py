# Generated by Django 3.1.1 on 2021-10-24 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0006_auto_20211018_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviemeta',
            name='type_code',
            field=models.CharField(db_index=True, default='', max_length=50),
        ),
    ]
