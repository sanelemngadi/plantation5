# Generated by Django 4.2.6 on 2023-10-30 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_plantationappointmentsmodel_assigned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantationappointmentsmodel',
            old_name='appointment_done',
            new_name='confirmed',
        ),
    ]
