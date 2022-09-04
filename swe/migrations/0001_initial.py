# Generated by Django 4.1 on 2022-09-04 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('code', models.CharField(db_index=True, default='', max_length=100)),
                ('name', models.CharField(db_index=True, default='', max_length=200)),
                ('description', models.TextField(null=True)),
                ('parent_code', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'code',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('email', models.CharField(db_index=True, default='', max_length=200)),
                ('profession', models.CharField(default='', max_length=50)),
                ('name', models.CharField(default='', max_length=50)),
                ('address', models.TextField(default='')),
                ('age', models.IntegerField(db_index=True, default=0)),
                ('sex', models.CharField(default='', max_length=10)),
                ('refresh_token', models.TextField(default='')),
                ('password', models.TextField(default='')),
                ('phone_no', models.CharField(default='', max_length=50)),
                ('role', models.CharField(default='user', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('title', models.CharField(db_index=True, default='', max_length=200)),
                ('director', models.CharField(db_index=True, default='', max_length=200)),
                ('release_date', models.DateTimeField()),
                ('total_view', models.IntegerField(default=0)),
                ('daily_view', models.IntegerField(default=0)),
                ('poster_path', models.TextField(default='')),
            ],
            options={
                'db_table': 'movie',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('movie', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.CASCADE, related_name='request', to='swe.movie')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='request', to='swe.member')),
            ],
            options={
                'db_table': 'request',
            },
        ),
        migrations.CreateModel(
            name='ReOpen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('movie', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.CASCADE, related_name='re_open', to='swe.movie')),
            ],
            options={
                'db_table': 're_open',
            },
        ),
        migrations.CreateModel(
            name='MovieMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('type_code', models.CharField(db_index=True, default='', max_length=50)),
                ('movie', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.CASCADE, related_name='movie_meta', to='swe.movie')),
            ],
            options={
                'db_table': 'movie_meta',
            },
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('image', models.TextField(default=True, null=True)),
                ('movie', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.CASCADE, related_name='movie_image_meta', to='swe.movie')),
            ],
            options={
                'db_table': 'movie_image',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(default='', max_length=50)),
                ('content', models.TextField(default='')),
                ('movie', models.ForeignKey(db_column='movie_id', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='swe.movie')),
                ('request', models.ForeignKey(db_column='request_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='swe.request')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='swe.member')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
