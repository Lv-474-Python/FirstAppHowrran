# Generated by Django 3.0.2 on 2020-01-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tbl_users',
            },
        ),
    ]
