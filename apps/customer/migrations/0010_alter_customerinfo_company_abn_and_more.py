# Generated by Django 4.1.2 on 2022-11-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_customerinfo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='company_ABN',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]