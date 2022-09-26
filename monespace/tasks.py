import datetime
from celery import shared_task
import environ

from .models import Event, AttendeesEvents, User, RecurringPattern, EventExceptionCancelledRescheduled, StatusUsersLocations
from .views_attend import get_count_event_specific
from .views_events import events_list, return_date_based_pattern
from .notification_manager import send_email


env = environ.Env()
# reading .env file
environ.Env.read_env()
email_gmail = env("email_gmail")


@shared_task()
def send_1_day_reminder_attend():
    today = datetime.datetime.now()
    days = 1
    days_added = datetime.timedelta(days=days)
    date_to = today + days_added
    # print(date_to.strftime("%Y-%m-%d"))
    attendees = AttendeesEvents.objects.filter(event_date=date_to.strftime("%Y-%m-%d"))
    list_users = []
    for y in attendees:
        # print(y.event_date)
        list_users.append(y.user)
    # print(list_users)
    send_email(5, list_users, email_gmail, date=date_to.strftime("%Y-%m-%d"))


@shared_task()
def send_2_days_reminder_non_attendees():
    today = datetime.datetime.now()
    days = 2
    days_added = datetime.timedelta(days=days)
    date_from = today + days_added
    date_from_bis = datetime.datetime(date_from.year, date_from.month, date_from.day)
    date_to = date_from_bis + datetime.timedelta(minutes=1439)
    events_to_check = events_list(date_from=date_from_bis, date_to=date_to)
    for i in events_to_check:
        distrib_date = Event.objects.get(uuid=i[1][0]['uuid'])
        nb_benev = get_count_event_specific(distrib_date, date_to.strftime("%Y-%m-%d"))
        if distrib_date.pre_alert_non_attendees_status and distrib_date.pre_alert_non_attendees_nb_attendees > nb_benev:
            list_users = []
            attendees = [y.user for y in AttendeesEvents.objects.filter(event_date=date_to.strftime("%Y-%m-%d"), parent_event=distrib_date)]
            for z in StatusUsersLocations.objects.filter(distrib=distrib_date):
                if z.user not in attendees:
                    list_users.append(z.user)
            # print(list_users)
            send_email(8, list_users, email_gmail, date=date_to.strftime("%Y-%m-%d"), distrib=distrib_date.name)


@shared_task()
def say_hello():
    print('bonjour')