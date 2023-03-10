# Generated by Django 4.0.4 on 2023-02-08 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0007_remove_admin_id_alter_admin_admin_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='body',
            name='Car_ID',
        ),
        migrations.AddField(
            model_name='car',
            name='Body_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_app.body'),
        ),
        migrations.AddField(
            model_name='engine',
            name='id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_app.cylinder'),
        ),
        migrations.AlterField(
            model_name='cylinder',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
