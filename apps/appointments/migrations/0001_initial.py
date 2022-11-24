# Generated by Django 4.1.2 on 2022-11-23 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_alter_userroles_company'),
        ('properties', '0003_businessdetails_business_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.appointmenttype')),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userroles')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_status', models.CharField(choices=[], max_length=255)),
                ('appointment_time', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('appointment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.appointmenttype')),
                ('field_worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userroles')),
                ('property_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
    ]