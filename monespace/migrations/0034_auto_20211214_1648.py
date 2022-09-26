# Generated by Django 3.2.9 on 2021-12-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0033_auto_20211214_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='event_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='groups',
            field=models.IntegerField(blank=True, choices=[(1, 'À tous'), (2, 'Aux présents'), (3, 'Aux non présents')], null=True),
        ),
    ]
