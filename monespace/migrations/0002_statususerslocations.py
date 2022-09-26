# Generated by Django 3.2.9 on 2021-11-09 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monespace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusUsersLocations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Active'), (3, 'Rejected'), (4, 'Deactivated')], default=1)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_status_user', to='monespace.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_status_location', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
