# Generated by Django 4.1 on 2022-09-12 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swe', '0007_member_remove_comment_user_remove_request_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('profession', models.CharField(default='', max_length=50)),
                ('address', models.TextField(default='')),
                ('age', models.IntegerField(db_index=True, default=0)),
                ('sex', models.CharField(default='', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='member',
        ),
        migrations.RemoveField(
            model_name='request',
            name='member',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(db_column='user_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(db_column='user_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='request', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
