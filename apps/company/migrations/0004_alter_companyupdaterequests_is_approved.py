# Generated by Django 4.1.2 on 2022-10-27 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_companyupdaterequests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyupdaterequests',
            name='is_approved',
            field=models.BooleanField(default=None, null=True),
        ),
    ]