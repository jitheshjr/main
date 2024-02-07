# Generated by Django 5.0.2 on 2024-02-07 14:42

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
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.SmallIntegerField()),
                ('floor', models.CharField(max_length=50)),
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
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.student')),
            ],
        ),
        migrations.CreateModel(
            name='Allotment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.room')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel.student')),
            ],
        ),
    ]
