# Generated by Django 4.1.5 on 2023-01-29 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='Admin_ID',
        ),
        migrations.AlterField(
            model_name='admin',
            name='salary',
            field=models.FloatField(),
        ),
    ]
