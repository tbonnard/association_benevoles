import json
from pprint import pprint
from collections import defaultdict
from collections import OrderedDict

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse

from .models import Event, Location, RecurringPattern, StatusUsersLocations, AttendeesEvents, \
    EventExceptionCancelledRescheduled, User
from .forms import EventForm, EventRecurringPatternForm, MessagesEventsSimpleForm
from .functions_global import forbidden_to_user, location_manager_check
from .notification_manager import send_email
from .views_distrib import get_last_attendance


def return_date_based_pattern(rec_pattern, date):
    event_date = date
    if rec_pattern.repeat_each_x == 0:
        event_date = event_date + datetime.timedelta(days=rec_pattern.separation_count * 7)
    elif rec_pattern.repeat_each_x == 1:
        event_date = event_date + datetime.timedelta(days=rec_pattern.separation_count * 1)
    elif rec_pattern.repeat_each_x == 2:
        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 4)
    elif rec_pattern.repeat_each_x == 3:
        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 12)
    elif rec_pattern.repeat_each_x == 4:
        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 24)
    elif rec_pattern.repeat_each_x == 5:
        event_date = event_date + datetime.timedelta(weeks=rec_pattern.separation_count * 56)
    return event_date


def events_list(date_from, date_to, location=None, event_manager=None, distrib=None, attendance=False, user_requester=None):
    """
    Get all events based on parameters
    :param date_from:
    :param date_to:
    :param location:
    :return: List of events - objects
    """

    if date_from is None:
        date_from = datetime.datetime.now().replace(minute=00, hour=00, second=00)
        # date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    else:
        date_from = date_from.replace(minute=00, hour=00, second=00)
        # date_from = date_from - datetime.timedelta(days=1)

    if date_to is None:
        days = 14
        days_added = datetime.timedelta(days=days)
        date_to_pre = date_from + days_added
        date_to=date_to_pre.replace(minute=59, hour=23, second=00)
    else:
        date_to = date_to.replace(minute=59, hour=23, second=00)

    if location is not None and event_manager is None and distrib is None:
        all_events = [i for i in Event.objects.filter(location=location)]
    elif location is None and event_manager is not None and distrib is None:
        all_events = [i for i in Event.objects.all() if event_manager in i.event_managers.all()]
    elif location is not None and event_manager is not None and distrib is None:
        all_events = [i for i in Event.objects.filter(location=location) if event_manager in i.event_managers.all()]
    elif location is not None and event_manager is None and distrib is not None:
        all_events = [Event.objects.get(pk=i.pk, location=location) for i in distrib]
    elif location is None and event_manager is not None and distrib is not None:
        all_events = [Event.objects.get(pk=i.pk) for i in distrib if event_manager in i.event_managers.all()]
    elif location is None and event_manager is None and distrib is not None:
        all_events = [Event.objects.get(pk=i.pk) for i in distrib]
    elif location is not None and event_manager is not None and distrib is not None:
        all_events = [Event.objects.get(location=location, pk=i.pk) for i in distrib if event_manager in i.event_managers.all()]
    else:
        all_events = Event.objects.all()

    eligible_events_date = dict()
    for j in all_events:
        event_date = j.start_date
        if j.is_recurring:
            try:
                rec_pattern = RecurringPattern.objects.get(event=j)
            except:
                continue
            for n in range(rec_pattern.max_num_occurrences + 1):
                if date_from <= datetime.datetime(event_date.year, event_date.month, event_date.day).replace(minute=j.time_from.minute, hour=j.time_from.hour, second=00) <= date_to:
                    if attendance:
                        if AttendeesEvents.objects.filter(user=user_requester, parent_event=j, event_date=datetime.datetime(event_date.year, event_date.month, event_date.day)):
                            if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j,
                                                                                     start_date=event_date):
                                try:
                                    eligible_events_date[event_date][str(j.uuid)] = {'details': j.serialize()}
                                except KeyError:
                                    eligible_events_date.setdefault(event_date, {str(j.uuid): {'details': j.serialize()} })

                    else:
                        try:
                            eligible_events_date[event_date][str(j.uuid)] = {'details': j.serialize() }
                            if EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j, start_date=event_date):
                                eligible_events_date[event_date][str(j.uuid)]['details']["event_date_cancelled"] = 1
                        except KeyError:
                            eligible_events_date.setdefault(event_date, { str(j.uuid): {'details': j.serialize() }})
                            if EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j, start_date=event_date):
                                eligible_events_date[event_date][str(j.uuid)]['details']["event_date_cancelled"] = 1
                event_date = return_date_based_pattern(rec_pattern, event_date)

        else:
            if date_from <= datetime.datetime(event_date.year, event_date.month, event_date.day) <= date_to:
                if attendance:
                    if AttendeesEvents.objects.filter(user=user_requester, parent_event=j, event_date=datetime.datetime(event_date.year, event_date.month, event_date.day)):
                        if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j,
                                                                                 start_date=event_date):
                            try:
                                eligible_events_date[event_date][str(j.uuid)] = {'details': j.serialize()}
                            except KeyError:
                                eligible_events_date.setdefault(event_date, {str(j.uuid): {'details': j.serialize()}})

                else:
                    try:
                        eligible_events_date[event_date][str(j.uuid)] = {'details': j.serialize() }
                        if EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j, start_date=event_date):
                            eligible_events_date[event_date][str(j.uuid)]['details']["event_date_cancelled"] = 1

                    except KeyError:
                        eligible_events_date.setdefault(event_date,{str(j.uuid): {'details': j.serialize()} })
                        if EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True, parent_event=j, start_date=event_date):
                            eligible_events_date[event_date][str(j.uuid)]['details']["event_date_cancelled"] = 1

    sorted_eligible_events_date = sorted(eligible_events_date.items())
    # pprint(sorted_eligible_events_date)
    return sorted_eligible_events_date


# USED BY JS
@login_required(login_url='/login/')
@forbidden_to_user
def events_list_json(request, user_id):
    try:
        date_from = datetime.datetime.strptime(request.GET['from'], '%Y-%m-%d')
    except:
        date_from = None
    try:
        date_to = datetime.datetime.strptime(request.GET['to'], '%Y-%m-%d')
    except:
        # date_to = datetime.datetime.now() - datetime.timedelta(days=1) + datetime.timedelta(days=14)
        date_to = datetime.datetime.now() + datetime.timedelta(days=14)
    events = events_list(date_from=date_from, date_to=date_to, location=None, event_manager=User.objects.get(uuid=user_id), distrib=None)
    return JsonResponse(events, safe=False)


@login_required(login_url='/login/')
def events_list_date(request):
    try:
        distrib = [Event.objects.get(uuid=request.GET['distrib'])]
    except:
        pre_user_distrib = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                             StatusUsersLocations.objects.filter(user=request.user, status=2)
        distrib = [i.distrib for i in pre_user_distrib]
    try:
        date_from = datetime.datetime.strptime(request.GET['from'], '%Y-%m-%d')
    except:
        date_from = None
    try:
        date_to = datetime.datetime.strptime(request.GET['to'], '%Y-%m-%d')
    except:
        days_added = datetime.timedelta(weeks=8)
        date_to = (datetime.datetime.now() + days_added)
    try:
        location = Location.objects.get(uuid=request.GET['location'])
    except:
        location = None
    finally:
        try:
            all_from_loc = request.GET['all']
            if all_from_loc != 'true':
                raise KeyError
        except:
            eligible_events_date = events_list(date_from=date_from, date_to=date_to, location=location,
                                               event_manager=None, distrib=distrib)
        else:
        # if request.user.user_type == 1:
        #     distrib = Event.objects.all()
            eligible_events_date = events_list(date_from=date_from, date_to=date_to, location=location, event_manager=None, distrib=None)
        attendees = AttendeesEvents.objects.filter(user=request.user)

    return render(request, 'all_events.html',
                  context={"events": eligible_events_date, "date_to": date_to.strftime("%Y-%m-%d"),
                           "attendees": attendees})


def create_event_unit(form):
    end_date = form.cleaned_data['end_date']
    if form.cleaned_data['end_date'] is None or form.cleaned_data['is_recurring']:
        end_date = form.cleaned_data['start_date']
    try:
        Location.objects.get(uuid=form['location'].value())
    except:
        location = None
    else:
        location = Location.objects.get(uuid=form['location'].value())
    finally:
        new_event = Event(name=form.cleaned_data['name'].title(),
                          description=form.cleaned_data['description'],
                          start_date=form.cleaned_data['start_date'],
                          end_date=end_date,
                          time_from=form.cleaned_data['time_from'],
                          time_to=form.cleaned_data['time_to'],
                          is_recurring=form.cleaned_data['is_recurring'],
                          is_full_day=form.cleaned_data['is_full_day'],
                          location=location,
                          event_managers=form.cleaned_data['event_managers']
                          )
        new_event.save()
        return new_event


def edit_event_unit(event, form):
    """
    Need the object of the event, not the ID
    :param: event: object to edit, form: form valid
    :return: return the event object
    """
    end_date = form.cleaned_data['end_date']
    if form.cleaned_data['end_date'] is None :
        end_date = form.cleaned_data['start_date']
    event.name = form.cleaned_data['name']
    event.description = form.cleaned_data['description']
    event.start_date = form.cleaned_data['start_date']
    event.end_date = end_date
    event.time_from = form.cleaned_data['time_from']
    event.time_to = form.cleaned_data['time_to']
    event.is_recurring = form.cleaned_data['is_recurring']
    event.is_full_day = form.cleaned_data['is_full_day']
    event.event_managers = form.cleaned_data['event_managers']
    try:
        Location.objects.get(uuid=form['location'].value())
    except:
        event.location = None
    else:
        event.location = Location.objects.get(uuid=form['location'].value())
    finally:
        event.save()
        return event


def create_recurring_pattern_event_unit(event, form):
    occur = form.cleaned_data['max_num_occurrences']
    if form.cleaned_data['max_num_occurrences'] == "":
        occur = 1
    count = form.cleaned_data['separation_count']
    if form.cleaned_data['separation_count'] == "":
        count = 1
    new_recurring = RecurringPattern(event=event,
                                     separation_count=count,
                                     max_num_occurrences=occur,
                                     # day_of_week=form.cleaned_data['day_of_week'],
                                     # week_of_month=form.cleaned_data['week_of_month'],
                                     # day_of_month=form.cleaned_data['day_of_month'],
                                     # month_of_year=form.cleaned_data['month_of_year'],
                                     repeat_each_x=form.cleaned_data['repeat_each_x']
                                     )
    new_recurring.save()
    return new_recurring


def edit_recurring_pattern_event_unit(recurring_pattern, form):
    """
    Need the object of the recurring pattern, not the ID
    :param: recurring_pattern: object to edit, form: form valid
    :return: the object recurring_pattern
    """
    occur = form.cleaned_data['max_num_occurrences']
    if form.cleaned_data['max_num_occurrences'] == "":
        occur = 1
    count = form.cleaned_data['separation_count']
    if form.cleaned_data['separation_count'] == "":
        count = 1
    recurring_pattern.separation_count = count
    recurring_pattern.max_num_occurrences = occur
    # recurring_pattern.day_of_week = form.cleaned_data['day_of_week']
    # recurring_pattern.week_of_month = form.cleaned_data['week_of_month']
    # recurring_pattern.day_of_month = form.cleaned_data['day_of_month']
    # recurring_pattern.month_of_year = form.cleaned_data['month_of_year']
    recurring_pattern.repeat_each_x = form.cleaned_data['repeat_each_x']
    recurring_pattern.save()
    return recurring_pattern


def default_initial_event_form(request, form, edit=False):
    if request.user.user_type == 1:
        form.fields['location'].queryset = Location.objects.all()
        user_from_location = Location.objects.all()
        if Location.objects.all().count() == 1:
            form.initial["location"] = Location.objects.all().first()
    else:
        form.fields['location'].queryset = Location.objects.all().filter(location_managers=request.user)
        user_from_location = Location.objects.all().filter(location_managers=request.user)
        if Location.objects.all().filter(location_managers=request.user).count() == 1:
            form.initial["location"] = Location.objects.all().filter(location_managers=request.user).first()
    users_loc = []
    for i in user_from_location:
        for y in i.location_managers.all():
            users_loc.append(y.uuid)
    form.fields['event_managers'].queryset = User.objects.filter(uuid__in=users_loc)
    # if not edit:
    #     if request.user.uuid in users_loc:
    #         form.initial["event_managers"] = request.user
    return form


@login_required(login_url='/login/')
@forbidden_to_user
def event_create(request):
    return redirect('index')
    # pre_form = EventForm()
    # form = default_initial_event_form(request, pre_form)
    # rec_form = EventRecurringPatternForm()
    # if request.method == "POST":
    #     form = EventForm(data=request.POST)
    #     rec_form = EventRecurringPatternForm(data=request.POST)
    #     if form.is_valid() and rec_form.is_valid():
    #         new_event = create_event_unit(form)
    #         if new_event.is_recurring:
    #             create_recurring_pattern_event_unit(event=new_event, form=rec_form)
    #         return redirect('index')
    # return render(request, 'event_create.html', context={"form": form, "rec_form": rec_form})


def validate_event_date(event, date):
    event_valid = False
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[-2:])
    date_in_datetime = datetime.datetime(year, month, day)
    date_in_date = datetime.date(year, month, day)
    if event.is_recurring:
        eligible_event_date = events_list(date_from=date_in_datetime, date_to=date_in_datetime, location=None, event_manager=None, distrib=None)
        for i in eligible_event_date:
            for (j, value) in i[1].items():
                if i[0] == date_in_date and value['details']['uuid'] == event.uuid:
                    event_valid = True
    else:
        if event.start_date == date_in_date:
            event_valid = True
    return event_valid


@login_required(login_url='/login/')
@forbidden_to_user
def event_edit(request, event_id):
    return redirect('index')
    # No need with new version
    # try:
    #     event_page = Event.objects.get(id=event_id)
    # except:
    #     redirect('index')
    # else:
    #     if request.method == "GET":
    #         pre_form = EventForm(instance=event_page)
    #         form = default_initial_event_form(request, pre_form, True)
    #         form.initial["start_date"] = event_page.start_date.strftime("%Y-%m-%d")
    #         form.initial["end_date"] = event_page.end_date.strftime("%Y-%m-%d")
    #         if event_page.is_recurring:
    #             event_rec_pattern = RecurringPattern.objects.filter(event=event_page).first()
    #             form.initial["start_date"] = request.GET.get('date')
    #             form.initial["end_date"] = request.GET.get('date')
    #             rec_form = EventRecurringPatternForm(instance=event_rec_pattern)
    #             if validate_event_date(event_page, request.GET.get('date')):
    #                 return render(request, 'event_edit_rec.html',
    #                               context={"form": form, "rec_form": rec_form, "event":event_page, "date":request.GET.get('date')})
    #             return redirect('index')
    #
    #         else:
    #             return render(request, 'event_edit_non_rec.html',
    #                           context={"form": form, "event":event_page})
    #
    #     if request.method == "POST":
    #         form = EventForm(data=request.POST)
    #         rec_form = EventRecurringPatternForm(data=request.POST)
    #         if form.is_valid() and rec_form.is_valid():
    #             event_page = edit_event_unit(event=event_page, form=form)
    #             if event_page.is_recurring:
    #                 if RecurringPattern.objects.filter(event=event_page).first():
    #                     rec_edit = edit_recurring_pattern_event_unit(
    #                         recurring_pattern=RecurringPattern.objects.filter(event=event_page).first(),
    #                         form=rec_form)
    #
    #                     # check to remove attendees if some dates have been removed
    #                     dates = [event_page.start_date]
    #                     date_new = event_page.start_date
    #                     for n in range(rec_edit.max_num_occurrences + 1):
    #                         max_date = return_date_based_pattern(rec_edit, date_new)
    #                         dates.append(max_date)
    #                         date_new = max_date
    #
    #                     all_attendees = AttendeesEvents.objects.filter(parent_event=event_page,
    #                                                                    recurring_pattern=rec_edit)
    #
    #                     for i in all_attendees:
    #                         if i.event_date not in dates or event_page.time_from != i.time_from or event_page.time_to != i.time_to:
    #                             i.delete()
    #
    #                 else:
    #                     create_recurring_pattern_event_unit(event=event_page, form=rec_form)
    #
    #                 return redirect('index')
    #
    #             else:
    #                 if RecurringPattern.objects.filter(event=event_page).first():
    #                     RecurringPattern.objects.filter(event=event_page).first().delete()
    #                     # attendees associated will be deleted (cascade)
    #
    #                 # remove attendees if date / hour are different
    #                 all_attendees_non_rec = AttendeesEvents.objects.filter(parent_event=event_page)
    #                 for i in all_attendees_non_rec:
    #                     if event_page.start_date != i.event_date or event_page.time_from != i.time_from or event_page.time_to != i.time_to :
    #                         i.delete()
    #
    #             return redirect('index')


@login_required(login_url='/login/')
@forbidden_to_user
def event_edit_specific_rec(request, event_id):
    return redirect('index')
    # No need with new version
    # try:
    #     event = Event.objects.get(pk=event_id)
    # except:
    #     return redirect('index')
    # else:
    #     if request.method == "POST":
    #
    #         form = EventForm(data=request.POST)
    #
    #         if form.is_valid():
    #             if validate_event_date(event, request.GET.get('date')):
    #
    #                 rec_to_delete_exception = EventExceptionCancelledRescheduled(
    #                     location=event.location,
    #                     name=event.name,
    #                     description=event.description,
    #                     start_date=request.GET.get('date'),
    #                     end_date=event.end_date,
    #                     time_from=event.time_from,
    #                     time_to=event.time_to,
    #                     is_cancelled=True,
    #                     is_rescheduled=True,
    #                     is_full_day=event.is_full_day,
    #                     parent_event=event,
    #                 )
    #                 rec_to_delete_exception.save()
    #
    #                 new_event = create_event_unit(form)
    #                 new_event.is_recurring = False
    #                 new_event.was_recurring_event_rec = event
    #                 new_event.save()
    #
    #             all_attendees_non_rec = AttendeesEvents.objects.filter(parent_event=event)
    #             for i in all_attendees_non_rec:
    #                 if new_event.start_date != i.event_date or new_event.time_from != i.time_from or new_event.time_to != i.time_to:
    #                     i.delete()
    #                 else:
    #                     i.parent_event = new_event
    #                     i.save()
    #
    #             return redirect('index')
    #         return redirect('index')
    #     return redirect('index')


@login_required(login_url='/login/')
def event_details(request, event_id):
    try:
        date = request.GET['date']
        event_page = Event.objects.get(uuid=event_id)
    except:
        return redirect('index')
    else:
        if validate_event_date(event_page, date):
            attendees = AttendeesEvents.objects.filter(user=request.user, parent_event=Event.objects.get(uuid=event_id),
                                                       event_date=date).first()
            all_attendees = AttendeesEvents.objects.filter(parent_event=Event.objects.get(uuid=event_id), event_date=date)
            count_attendees = all_attendees.count()
            for i in all_attendees:
                count_attendees += i.plus_other
            manager_location = False
            for i in event_page.location.location_managers.all():
                if i == request.user:
                    manager_location = True
            message_form = MessagesEventsSimpleForm()
            date_cancelled = False
            if EventExceptionCancelledRescheduled.objects.filter(parent_event=event_page, start_date=date).first():
                date_cancelled = True

            all_attendees_users = [i.user for i in all_attendees]
            users_from_status_users_location_dict = get_last_attendance(all_attendees_users, event_page)

            return render(request, 'event_details.html',
                              context={"event": event_page, "manager_location": manager_location, 'date': date,
                                       "attendees": attendees, "all_attendees": all_attendees,
                                       "count_attendees": count_attendees, "message_form":message_form,
                                       "cancelled":date_cancelled, "last_attendance":users_from_status_users_location_dict})
        return redirect('index')


def check_to_delete(event_to_delete, requested_user):
    new_number_occurences = 0
    if event_to_delete.is_recurring:
        rec_pattern = RecurringPattern.objects.filter(event=event_to_delete).first()
        event_date = event_to_delete.start_date
        for n in range(rec_pattern.max_num_occurrences + 1):
            if datetime.datetime(event_to_delete.start_date.year, event_to_delete.start_date.month, event_to_delete.start_date.day).replace(minute=event_to_delete.time_to.minute, hour=event_to_delete.time_to.hour, second=00) <= datetime.datetime(event_date.year, event_date.month, event_date.day).replace(minute=event_to_delete.time_to.minute, hour=event_to_delete.time_to.hour, second=00) <= datetime.datetime.now():
                new_number_occurences += 1
                # if not EventExceptionCancelledRescheduled.objects.filter(is_cancelled=True,
                #                                                          parent_event=event_to_delete,
                #                                                          start_date=event_date):
                #     new_number_occurences += 1
                # else:
                #     continue

            if datetime.datetime(event_date.year, event_date.month, event_date.day).replace(minute=event_to_delete.time_from.minute, hour=event_to_delete.time_from.hour, second=00) >= datetime.datetime.now():
                for i in AttendeesEvents.objects.filter(parent_event=event_to_delete, event_date=event_date):
                    send_email(6, [i.user], requested_user, distrib=event_to_delete.name, date=event_date)
                    i.delete()
                    # or update status in attendees to 0 if we want to keep history

            event_date = return_date_based_pattern(rec_pattern, event_date)

        # no need anymore -->
        # rec_event_updated_to_specific_date = Event.objects.filter(was_recurring_event_rec=event_to_delete)
        # for i in rec_event_updated_to_specific_date:
        #     if datetime.datetime(i.start_date.year, i.start_date.month, i.start_date.day) > datetime.datetime.now():
        #         i.delete()

        rec_pattern.max_num_occurrences = new_number_occurences - 1
        rec_pattern.save()

    if new_number_occurences == 0:
        event_to_delete.delete()

    return new_number_occurences


@login_required(login_url='/login/')
@forbidden_to_user
@location_manager_check
def event_delete_all(request, event_id):
    try:
        event_to_delete = Event.objects.get(uuid=event_id)
    except:
        return redirect('index')
    else:
        event_to_delete.is_cancelled = True
        event_to_delete.save()
        check_to_delete(event_to_delete, request.user)
        return redirect('index')


@login_required(login_url='/login/')
@forbidden_to_user
@location_manager_check
def event_delete_rec(request, event_id):
    try:
        # print('1')
        date = request.GET['date']
        event_rec_to_delete = Event.objects.get(uuid=event_id)
    except:
        # print('2')
        return redirect('index')
    else:
        # print('3')
        if EventExceptionCancelledRescheduled.objects.filter(parent_event=event_rec_to_delete, start_date=date).first():
            rec_to_delete_exception = EventExceptionCancelledRescheduled.objects.filter(parent_event=event_rec_to_delete, start_date=date).first()
            rec_to_delete_exception.is_cancelled=True
        else:
            rec_to_delete_exception = EventExceptionCancelledRescheduled(
                location=event_rec_to_delete.location,
                name=event_rec_to_delete.name,
                description=event_rec_to_delete.description,
                start_date=date,
                end_date=event_rec_to_delete.end_date,
                time_from=event_rec_to_delete.time_from,
                time_to=event_rec_to_delete.time_to,
                is_cancelled=True,
                is_rescheduled=False,
                is_full_day=event_rec_to_delete.is_full_day,
                parent_event=event_rec_to_delete,
            )
        rec_to_delete_exception.save()
        for i in AttendeesEvents.objects.filter(parent_event=event_rec_to_delete, event_date=date):
            send_email(6, [i.user], request.user, distrib=event_rec_to_delete.name, date=date)
            i.delete()
            # or update status in attendees to 0 if we want to keep history
        return redirect('index')


@login_required(login_url='/login/')
@forbidden_to_user
@location_manager_check
def reactivate_event_date(request, event_id):
    try:
        date = request.GET['date']
        exception_event_to_undo = EventExceptionCancelledRescheduled.objects.get(parent_event=Event.objects.get(uuid=event_id), start_date=date)
    except:
        return redirect('index')
    else:
        exception_event_to_undo.delete()
        return redirect('index')
