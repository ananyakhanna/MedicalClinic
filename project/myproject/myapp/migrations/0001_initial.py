# Generated by Django 4.0.6 on 2022-09-08 12:00

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_patient', models.BooleanField(default=False, verbose_name='Is Patient')),
                ('is_doctor', models.BooleanField(default=False, verbose_name='Is Doctor')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactno', models.BigIntegerField()),
                ('type', models.CharField(choices=[('Inpatient', 'Inpatient'), ('Outpatient', 'Outpatient')], max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('time', models.TimeField(blank=True, default=datetime.datetime.now)),
                ('services', models.TextField()),
                ('sent_date', models.DateField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('checkupstatus', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_date'],
            },
        ),
        migrations.CreateModel(
            name='Docinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docID', models.BigIntegerField()),
                ('docname', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('contactNo', models.BigIntegerField()),
                ('department', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ipbilling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billNo', models.BigIntegerField()),
                ('patientID', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('doa', models.DateField(blank=True, default=datetime.datetime.now)),
                ('dod', models.DateField(blank=True, default=datetime.datetime.now)),
                ('gender', models.CharField(max_length=100)),
                ('roomCharge', models.FloatField()),
                ('docFees', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Ipreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=500)),
                ('contactNo', models.BigIntegerField()),
                ('regDate', models.DateField(blank=True, default=datetime.datetime.now)),
                ('roomNo', models.IntegerField()),
                ('gender', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Opbilling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billNo', models.BigIntegerField()),
                ('patientID', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('docname', models.CharField(max_length=100)),
                ('coamt', models.FloatField()),
                ('totalamt', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Opreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('contactNo', models.BigIntegerField()),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('department', models.CharField(max_length=100)),
                ('docName', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pathology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=100)),
                ('testname', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Roominfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomNo', models.IntegerField()),
                ('roomType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=b'I01\n', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=20)),
                ('speciality', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=b'I01\n', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor_Summery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illness', models.CharField(max_length=100)),
                ('medication', models.CharField(max_length=1000)),
                ('dosage', models.CharField(max_length=500)),
                ('vaccination', models.CharField(max_length=500)),
                ('note', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.appointment')),
            ],
        ),
    ]
