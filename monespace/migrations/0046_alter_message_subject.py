# Generated by Django 3.2.9 on 2021-12-22 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0045_rename_to_event_manger_group_message_to_event_manager_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(default='', max_length=255),
        ),
    ]
