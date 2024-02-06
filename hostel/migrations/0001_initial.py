# Generated by Django 5.0.1 on 2024-02-04 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_id', models.SmallIntegerField()),
                ('dept_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pgm_id', models.SmallIntegerField()),
                ('pgm_name', models.CharField(max_length=100)),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.department')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=20)),
                ('pgm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.programme')),
            ],
        ),
    ]
