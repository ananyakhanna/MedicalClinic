# Generated by Django 4.0.6 on 2022-09-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_billing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billing',
            old_name='docFees',
            new_name='docFee',
        ),
    ]