# Generated by Django 3.2.9 on 2021-12-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0030_alter_logsstatususerslocations_distrib'),
    ]

    operations = [
        migrations.AddField(
            model_name='logsstatususerslocations',
            name='is_at_time_event_manager',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2021-12-11'),
        ),
    ]