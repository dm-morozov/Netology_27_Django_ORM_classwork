# Generated by Django 5.1 on 2024-08-20 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orm_second_part', '0002_orderposition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
