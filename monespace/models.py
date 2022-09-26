import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

country_list = (("FR", 'France'),)


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user_type_choices = ((1, 'Admin'), (2, 'User'), (3, 'Manager'))
    user_type = models.IntegerField(choices=user_type_choices, null=False, blank=False, default=2)
    address = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=255)
    zip_code = models.CharField(blank=True, null=True, max_length=5)
    country = models.CharField(choices=country_list, blank=True, null=True, max_length=2, default='FR')
    tel = models.CharField(blank=True, null=True, max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        if self.first_name is None or self.first_name == '':
            return f"{self.username}"
        else:
            return f"{self.first_name} {self.last_name}"

    def save_image(self, new_image):
        # Opening the uploaded image
        im = Image.open(new_image)

        output = BytesIO()

        # Resize/modify the image
        width_img = im.width
        height_img = im.height
        while width_img > 500 or height_img > 500:
            im = im.resize((width_img//2, height_img//2))
            width_img = im.width
            height_img = im.height

        # after modifications, save it to the output
        im.save(output, format='PNG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.profile_picture = InMemoryUploadedFile(output, 'ImageField', "%s.png" % new_image.name.split('.')[0], 'image/png',
                                        sys.getsizeof(output), None)

        super(User, self).save()


class Location(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, max_length=255)
    address = models.CharField(blank=False, max_length=255)
    address_2 = models.CharField(blank=True, max_length=255, default="")
    city = models.CharField(blank=False, max_length=255)
    zip_code = models.CharField( blank=False, max_length=5)
    country = models.CharField(choices=country_list, blank=False, max_length=2, default='FR')
    created = models.DateTimeField(auto_now_add=True)
    location_managers = models.ManyToManyField(User, blank=False)

    def __str__(self):
        return self.name

    def serialize(self):
        return {"uuid": self.uuid,
                "name": self.name,
                }


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=False, related_name="events_locations")
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField( blank=False, default=datetime.datetime.now().strftime("%Y-%m-%d"))
    end_date = models.DateField( blank=True, null=True)
    time_from = models.TimeField(blank=False, default="00:00:00")
    time_to = models.TimeField(blank=False, default="00:00:00")
    is_full_day = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    was_recurring_event_rec = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_distrib = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    event_managers = models.ManyToManyField(User, blank=False)
    pre_alert_non_attendees_nb_attendees = models.IntegerField(null=False, blank=False, default=20)
    pre_alert_non_attendees_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def serialize(self):
        return {"uuid": self.uuid,
                "name": self.name,
                "location": self.location.serialize(),
                "start_date": self.start_date,
                "time_from": self.time_from,
                "time_to": self.time_to,
                "event_cancelled": self.is_cancelled,
                "event_date_cancelled":0
                }


class RecurringPattern(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True)
    separation_count = models.IntegerField(blank=True, null=True)
    repeat_each_x = models.IntegerField(blank=True, null=True)
    # day_of_week = models.IntegerField(blank=True, null=True)
    # week_of_month = models.IntegerField(blank=True, null=True)
    # day_of_month = models.IntegerField(blank=True, null=True)
    # month_of_year = models.IntegerField(blank=True, null=True)
    max_num_occurrences = models.IntegerField(blank=True, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)


class EventExceptionCancelledRescheduled(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=False, related_name="events_exceptions_locations")
    name = models.CharField( blank=False, max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField( blank=False, default=utils.timezone.now)
    end_date = models.DateField( blank=True, null=True)
    time_from = models.TimeField(blank=True, default="00:00:00")
    time_to = models.TimeField(blank=True, default="00:00:00")
    is_cancelled = models.BooleanField(default=False)
    is_rescheduled = models.BooleanField(default=False)
    is_full_day = models.BooleanField(default=False)
    parent_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True, related_name="EventExceptionCancelledRescheduled_event")
    created = models.DateTimeField(auto_now_add=True)


class AttendeesEvents(models.Model):
    parent_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=True, related_name="AttendeesEvents_event")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    status = models.IntegerField(blank=False, null=False, default=1)
    event_date = models.DateField(blank=False, null=False, default=utils.timezone.now)
    plus_other = models.IntegerField(blank=True, null=False, default=0)
    recurring_pattern = models.ForeignKey(RecurringPattern, on_delete=models.CASCADE, blank=True, null=True)
    time_from = models.TimeField(blank=True, default="00:00:00")
    time_to = models.TimeField(blank=True, default="00:00:00")
    created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {"id": self.id,
                "parent_event": self.parent_event.uuid,
                "user": self.user.uuid,
                "event_date": self.event_date,
                "plus_other": self.plus_other,
                }


class StatusUsersLocations(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="location_status_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False,
                             related_name="user_status_location")
    status_choices = ((1, 'En attente'), (2, 'Actif'), (3, 'Rejeté'), (4, 'Désactivé'), (5, "Annulé par l'utilisateur"))
    status = models.IntegerField(choices=status_choices, null=False, blank=False, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    distrib = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="event_status_user")

    def __str__(self):
        return f"{self.user} - {self.location} - {self.distrib} - {self.status}"

    def __repr__(self):
        return f"{self.user} - {self.location} - {self.distrib} - {self.status}"

    def serialize(self):
        return {"id": self.id,
                "id_distrib": self.distrib.uuid,
                "location_id": self.location.uuid,
                "distrib":self.distrib.serialize(),
                "user_id":self.user.uuid,
                "user_status": self.status,
                }


class LogsStatusUsersLocations(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="Logs_location_status_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False,
                             related_name="logs_user_status_location")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True,
                             related_name="logs_fromuser_status_location")
    status_choices = ((1, 'En attente'), (2, 'Actif'), (3, 'Rejeté'), (4, 'Désactivé'), (5, "Annulé par l'utilisateur"))
    status = models.IntegerField(choices=status_choices, null=False, blank=False, default=1)
    current_status = models.IntegerField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    distrib = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="Logs_distrib_status_user")
    is_at_time_event_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"Log: {self.user} - {self.location} - {self.status}"

    def __repr__(self):
        return f"Log: {self.user} - {self.location} - {self.status}"


class Message(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    subject = models.CharField(blank=False, default="", max_length=255)
    description = models.TextField(blank=False, default="")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="messages_from_user")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, related_name="Messages_location")
    to_event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, related_name="Messages_event")
    to_event_date = models.DateField(blank=True, null=True)
    group_choices = ((1, 'À tous'), (2, 'Aux présents'), (3, 'Aux non présents'))
    to_event_group = models.IntegerField(choices=group_choices, null=True, blank=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="message_to_user")
    info_all_locations = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    group_choices_manager = ((1, 'Aux responsables'), (2, 'Aux bénévoles et responsables'))
    to_event_manager_group = models.IntegerField(choices=group_choices_manager, null=True, blank=True)

    def serialize(self):
        return {
                "uuid": self.uuid,
                }


class MessageSeen(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=False, null=False, related_name="messages_seen_message")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="messages_seen_user")
    date_seen = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
