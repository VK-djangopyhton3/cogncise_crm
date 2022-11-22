# Generated by Django 4.1.2 on 2022-11-22 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='is_business',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='lga',
            field=models.CharField(default='vic', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='business_details',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='properties.businessdetails'),
            preserve_default=False,
        ),
    ]
