import datetime

from celery.utils.serialization import jsonify
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import DistributionForm, StatusUsersLocationsForm, DistributionManagerForm, MessagesEventsSimpleForm, MessagesEventsManagerDistrib
from .functions_global import forbidden_to_user
from .models import Location, Event, RecurringPattern, StatusUsersLocations, LogsStatusUsersLocations, User, AttendeesEvents
from .notification_manager import send_email
from .views_locations import edit_user_type_to_manager, check_if_new_status_to_create_update, edit_user_type_to_user


@login_required(login_url='/login/')
@forbidden_to_user
def distribution_create(request, location_id):
    location = get_object_or_404(Location, uuid=location_id)
    form = DistributionForm()
    user_from_location = [i.uuid for i in Location.objects.get(uuid=location_id).location_managers.all()]
    form.fields['event_managers'].queryset = User.objects.filter(uuid__in=user_from_location)
    # if len(user_from_location) == 1:
    #     form.initial['event_managers'] = User.objects.get(uuid=user_from_location[0])

    if request.method == "POST":
        form = DistributionForm(data=request.POST)
        if form.is_valid():
            new_event = Event(name=form.cleaned_data['name'], start_date=form.cleaned_data['start_date'],
                              end_date=form.cleaned_data['start_date'],
                              location=location,
                              time_from=form.cleaned_data['time_from'], time_to=form.cleaned_data['time_to'],
                              is_recurring=True, is_distrib=True)
            new_event.save()
            managers = form.cleaned_data['event_managers']
            for i in managers:
                new_event.event_managers.add(i)
            new_event.save()

            new_rec = RecurringPattern(event=new_event, separation_count=1, max_num_occurrences=260, repeat_each_x=0)
            new_rec.save()

            for i in new_event.event_managers.all():
                edit_user_type_to_manager(i)
                check_if_new_status_to_create_update(distrib=new_event, location=new_event.location,
                                                 user_to_update=i, from_user=request.user,
                                                 manager=True)
            return redirect('index')
    return render(request, 'distrib_create.html', context={"form": form, "location": location})


@forbidden_to_user
@login_required(login_url='/login/')
def distributions(request):
    message_form = MessagesEventsManagerDistrib()
    # if request.user.user_type == 1:
    #     events = Event.objects.all()
    #     return render(request, 'distributions.html', context={"events": events})
    # if Event.objects.filter(event_manager=request.user).count() == 1:
    #     return redirect(reverse('distrib_details', kwargs={'distrib_id': Event.objects.filter(event_manager=request.user).first().pk}))
    # else:
    events = [i for i in Event.objects.all() if request.user in i.event_managers.all()]
    return render(request, 'distributions.html', context={"events": events, "message_form":message_form})


@login_required(login_url='/login/')
@forbidden_to_user
def distrib_details(request, distrib_id):
    distrib = get_object_or_404(Event, uuid=distrib_id)
    if distrib.is_cancelled:
        return redirect('index')
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')
    else:
        user_from_location = [i.uuid for i in Location.objects.get(uuid=distrib.location.uuid).location_managers.all()]
        formManager = DistributionManagerForm(instance=distrib)
        formManager.fields['event_managers'].queryset = User.objects.filter(uuid__in=user_from_location)

    return render(request, 'distrib_details.html', context={"distrib":distrib, "formManager":formManager})


@login_required(login_url='/login/')
@forbidden_to_user
def distrib_users(request, distrib_id):
    message_form = MessagesEventsSimpleForm()
    distrib = get_object_or_404(Event, uuid=distrib_id)
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(distrib=distrib, status=1) | \
                                StatusUsersLocations.objects.filter(distrib=distrib, status=2)
        form = StatusUsersLocationsForm()

        users_from_status_users_location = [i.user for i in status_users_location]
        users_from_status_users_location_dict = get_last_attendance(users_from_status_users_location, distrib)

    if request.method == "POST":
        try:
            user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
        except:
            pass
        else:
            user_status_update.status = 2
            user_status_update.save()
            logs = LogsStatusUsersLocations(distrib=distrib, location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=2, current_status=user_status_update.status)
            logs.save()
            send_email(3, [user_status_update.user], request.user, distrib=user_status_update.distrib.name)
            return redirect(reverse('distrib_users', kwargs={'distrib_id': distrib_id}))

    return render(request, 'benevoles_distrib.html', context={"distrib":distrib,
                                                            "status_users_location": status_users_location.order_by('user__first_name'),
                                                            "form": form, "message_form":message_form,
                                                              "last_attendance":users_from_status_users_location_dict})


def get_last_attendance(users, distrib):
    users_from_status_users_location_dict = {}
    for i in users:
        last_attendance = AttendeesEvents.objects.filter(parent_event=distrib, user=i,
                                                         event_date__lte=datetime.datetime.now()).order_by(
            'event_date').last()
        if last_attendance is not None:
            users_from_status_users_location_dict.setdefault(i.uuid, last_attendance.event_date)
    return users_from_status_users_location_dict


@login_required(login_url='/login/')
@forbidden_to_user
def user_distrib_update_status(request, distrib_id):
    if request.method == "POST":
        try:
            user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
            distrib_user = get_object_or_404(Event, uuid=distrib_id)
        except:
            pass
        else:
            user_status_update.status = request.POST['status']
            user_status_update.save()
            logs = LogsStatusUsersLocations(distrib=distrib_user, location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=request.POST['status'], current_status=user_status_update.status)
            logs.save()
            user_status_int = int(user_status_update.status)
            if user_status_int == 3:
                send_email(4, [user_status_update.user], request.user, distrib=user_status_update.distrib.name)

            return redirect(reverse('distrib_users', kwargs={'distrib_id': distrib_id}))
    return redirect('index')


@login_required(login_url='/login/')
@forbidden_to_user
def change_distrib_manager(request, distrib_id):
    distrib = get_object_or_404(Event, uuid=distrib_id)
    if request.user.user_type == 3 and request.user not in distrib.location.location_managers.all():
        return redirect('index')

    if request.method == "POST":
        form = DistributionManagerForm(data=request.POST)
        # check if no past distrib or not
        # cancel next ones and create a new one if already some in the past
        # update if no one past
        if form.is_valid():
            if distrib.time_from != form.cleaned_data['time_from'] or distrib.time_to != form.cleaned_data['time_to']:
                from .views_events import return_date_based_pattern
                event_date = distrib.start_date
                if distrib.is_recurring:
                    rec_pattern = RecurringPattern.objects.get(event=distrib)
                    need_to_delete = False
                    for n in range(rec_pattern.max_num_occurrences + 1):
                        if AttendeesEvents.objects.filter(parent_event=distrib, event_date=datetime.datetime(event_date.year, event_date.month, event_date.day)):
                            need_to_delete = True
                            break
                        event_date = return_date_based_pattern(rec_pattern, event_date)
                    if need_to_delete:
                        from .views_events import check_to_delete
                        check_to_delete(distrib, request.user)
                        new_event = Event(name=distrib.name, start_date=distrib.start_date,
                                          end_date=distrib.start_date,
                                          location=distrib.location,
                                          time_from=form.cleaned_data['time_from'],
                                          time_to=form.cleaned_data['time_to'],
                                          is_recurring=True, is_distrib=True,
                                          pre_alert_non_attendees_status=form.cleaned_data['pre_alert_non_attendees_status'],
                                        pre_alert_non_attendees_nb_attendees=form.cleaned_data['pre_alert_non_attendees_nb_attendees'])
                        new_event.save()
                        managers = form.cleaned_data['event_managers']
                        for i in managers:
                            new_event.event_managers.add(i)
                        new_event.save()

                        new_rec = RecurringPattern(event=new_event, separation_count=1, max_num_occurrences=260,
                                                   repeat_each_x=0)
                        new_rec.save()

                        for i in new_event.event_managers.all():
                            edit_user_type_to_manager(i)
                            check_if_new_status_to_create_update(distrib=new_event, location=new_event.location,
                                                                 user_to_update=i, from_user=request.user,
                                                                 manager=True)
                        distrib.is_cancelled = True
                        distrib.save()
                        return redirect(reverse('distrib_details', kwargs={'distrib_id': new_event.uuid}))


            else:
                distrib = get_object_or_404(Event, uuid=distrib_id)
                distrib.time_from = form.cleaned_data['time_from']
                distrib.time_to = form.cleaned_data['time_to']
                distrib.pre_alert_non_attendees_status = form.cleaned_data['pre_alert_non_attendees_status']
                distrib.pre_alert_non_attendees_nb_attendees = form.cleaned_data['pre_alert_non_attendees_nb_attendees']
                previous_manager = distrib.event_managers.all()
                managers = form.cleaned_data['event_managers']

                for i in managers:
                    if i not in previous_manager:
                        distrib.event_managers.add(i)
                        edit_user_type_to_manager(i)
                        check_if_new_status_to_create_update(distrib=distrib, location=distrib.location,
                                                             user_to_update=i, from_user=request.user,
                                                             manager=True)
                for i in previous_manager:
                    if i not in managers:
                        distrib.event_managers.remove(i)
                        edit_user_type_to_user(i)
                        check_if_new_status_to_create_update(distrib=distrib, location=distrib.location,
                                                             user_to_update=i, from_user=request.user,
                                                             manager=True)
                distrib.save()

            return redirect(reverse('distrib_details', kwargs={'distrib_id': distrib_id}))
    return redirect('index')


@login_required(login_url='/login/')
def get_event_location(request):
    all_event_distrib = Event.objects.filter(is_distrib=True, is_cancelled=False)
    return JsonResponse([i.serialize() for i in all_event_distrib], safe=False)


@login_required(login_url='/login/')
def get_user_distrib(request):
    status_user_distrib = StatusUsersLocations.objects.filter(user=request.user,
                                                                status=1) | StatusUsersLocations.objects.filter(
        user=request.user, status=2)
    return JsonResponse([i.serialize() for i in status_user_distrib.order_by('user__first_name')], safe=False)


@login_required(login_url='/login/')
def get_count_event_location(request, location_id):
    location = get_object_or_404(Location, uuid=location_id)
    event_loc_count = Event.objects.filter(is_distrib=True, is_cancelled=False, location=location).count()
    return JsonResponse(event_loc_count, safe=False)


@login_required(login_url='/login/')
@forbidden_to_user
def get_count_event_benev(request):
    status_user_distrib = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    count_distrib_ben = {}
    for i in status_user_distrib:
        if str(i.distrib.uuid) in count_distrib_ben:
            if i.status == 1:
                count_distrib_ben[str(i.distrib.uuid)]['pending'] += 1
            else:
                count_distrib_ben[str(i.distrib.uuid)]['active'] += 1
        else:
            if i.status == 1:
                count_distrib_ben.setdefault(str(i.distrib.uuid), {"pending":1, "active":0})
            else:
                count_distrib_ben.setdefault(str(i.distrib.uuid), {"pending":0, "active":1})
    return JsonResponse(count_distrib_ben, safe=False)