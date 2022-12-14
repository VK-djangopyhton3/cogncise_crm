# Generated by Django 4.1.2 on 2022-11-18 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='StreetTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(max_length=255)),
                ('level_no', models.IntegerField(blank=True, null=True)),
                ('unit_no', models.IntegerField(blank=True, null=True)),
                ('lot_no', models.IntegerField(blank=True, null=True)),
                ('street_name', models.CharField(max_length=255)),
                ('suffix', models.CharField(max_length=255)),
                ('suburb', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_billing_address', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customerinfo')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.propertytypes')),
                ('street_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.streettypes')),
            ],
        ),
        migrations.AddConstraint(
            model_name='property',
            constraint=models.UniqueConstraint(condition=models.Q(('is_billing_address', True)), fields=('customer',), name='unique_billing_address'),
        ),
    ]
