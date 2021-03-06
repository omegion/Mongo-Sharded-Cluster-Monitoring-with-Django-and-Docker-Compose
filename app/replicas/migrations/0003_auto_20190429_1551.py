# Generated by Django 2.2 on 2019-04-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replicas', '0002_auto_20190429_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(default=0, max_length=10)),
                ('memory', models.CharField(default=0, max_length=10)),
                ('io', models.CharField(default=0, max_length=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='replica',
            name='cpu',
        ),
        migrations.RemoveField(
            model_name='replica',
            name='io',
        ),
        migrations.RemoveField(
            model_name='replica',
            name='memory',
        ),
    ]
