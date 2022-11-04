# Generated by Django 4.0.6 on 2022-09-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_mcqtest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.CharField(choices=[('Dermatology', 'Dermatology'), ('Gastroenterology', 'Gastroenterology'), ('Neurology', 'Neurology'), ('Obsterics/Gynecology', 'Obsterics/Gynecology'), ('Pediatrics', 'Pediatrics'), ('Ophthalmology', 'Ophthalmology'), ('Psychiatry', 'Psychiatry'), ('Urology', 'Urology'), ('Emergency medicine', 'Emergency_medicine')], max_length=50),
        ),
    ]
