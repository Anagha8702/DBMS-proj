# Generated by Django 4.1.5 on 2023-02-14 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0009_customer_age_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='bought_by',
            name='rating',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]