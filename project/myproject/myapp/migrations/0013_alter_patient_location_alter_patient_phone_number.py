# Generated by Django 4.0.6 on 2022-09-21 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_appointment_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]
