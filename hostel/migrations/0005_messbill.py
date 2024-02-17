# Generated by Django 5.0.1 on 2024-02-16 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0004_alter_allotment_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_students', models.SmallIntegerField()),
                ('month', models.CharField(max_length=42)),
                ('mess_days', models.SmallIntegerField()),
                ('mess_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('staff_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('electricity_bill', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]