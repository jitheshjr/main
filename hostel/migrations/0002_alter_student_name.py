# Generated by Django 5.0.2 on 2024-02-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
