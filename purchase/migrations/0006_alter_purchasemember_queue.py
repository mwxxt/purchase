# Generated by Django 5.0.2 on 2024-03-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_alter_purchasemember_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasemember',
            name='queue',
            field=models.PositiveBigIntegerField(blank=True, unique=True, verbose_name='Очередь'),
        ),
    ]
