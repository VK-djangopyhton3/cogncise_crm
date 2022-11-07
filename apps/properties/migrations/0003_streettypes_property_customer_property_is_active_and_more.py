# Generated by Django 4.1.2 on 2022-11-07 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_remove_customerinfo_agency_and_more'),
        ('properties', '0002_rename_unit_type_propertytypes_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreetTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='customer',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='customer.customerinfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='properties.propertytypes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertytypes',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='street_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.streettypes'),
        ),
    ]
