# Generated by Django 5.1 on 2024-08-16 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_alter_location_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('name', 'type')},
        ),
    ]
