# Generated by Django 5.2.3 on 2025-06-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZodiacSign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('element', models.CharField(max_length=20)),
                ('ruling_planet', models.CharField(max_length=50)),
            ],
        ),
    ]
