# Generated by Django 4.2.6 on 2023-10-28 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
        ('products', '0003_delete_plantationimagevariation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantationproduct',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='suppliers.plantationsupplier'),
        ),
    ]
