# Generated by Django 3.2.9 on 2021-11-10 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0004_auto_20211110_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='statususerslocations',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
