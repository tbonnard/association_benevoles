# Generated by Django 3.2.9 on 2021-12-03 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0020_rename_test_user_location_locations_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='locations_managers',
            new_name='location_managers',
        ),
    ]
