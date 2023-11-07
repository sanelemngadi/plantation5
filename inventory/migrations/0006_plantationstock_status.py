# Generated by Django 4.2.6 on 2023-11-05 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_remove_plantationstock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantationstock',
            name='status',
            field=models.CharField(choices=[('P', 'Pending for delivery'), ('D', 'Delivered')], default='P', max_length=2),
        ),
    ]
