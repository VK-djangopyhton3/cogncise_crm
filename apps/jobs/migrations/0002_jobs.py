# Generated by Django 4.1.2 on 2022-11-28 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_remove_property_business_details_and_more'),
        ('customer', '0008_remove_customerinfo_type'),
        ('users', '0004_alter_userroles_company'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_status', models.CharField(choices=[('New Job', 'New Job'), ('Won', 'Won')], default='New Lead', max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userroles')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customerinfo')),
                ('property_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
                ('work_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.worktype')),
            ],
        ),
    ]
