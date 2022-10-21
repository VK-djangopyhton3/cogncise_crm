from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('company_address', models.CharField(max_length=255)),
                ('ABN', models.CharField(max_length=255, null=True, unique=True)),
            ],
        ),
    ]