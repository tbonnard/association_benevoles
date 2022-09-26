from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Location, StatusUsersLocations, LogsStatusUsersLocations, Event, AttendeesEvents
from .forms import LocationForm, SelectLocationsForm, MessagesEventsSimpleForm, MessagesEventsManagerDistrib
from .notification_manager import send_email
from .functions_global import forbidden_to_user, admin_only


def edit_user_type_to_manager(user):
    if user.user_type != 1:
        user.user_type = 3
        user.save()


def edit_user_type_to_user(user):
    """
    Edit user that is currently manager to another user type ("user")
    If user have multi-sites, he remains manager
    :param user: user for which we want to update status
    :return:
    """
    if user.user_type != 1:
        user_manager_other_location = Location.objects.filter(location_managers=user)
        if user_manager_other_location.count() == 0:
            user.user_type = 2
            user.save()


def check_if_new_status_to_create_update(distrib, location, user_to_update, from_user, manager=False):
    """
    Check if the status-location of the user must be updated depending on:
    - user is/becomes a manager
    - user is a user and asks to be part of the location
    - user already has other status (rejected, declined, ...)
    :param location: location object for which the status might be updated
    :param user_to_update: user object for which the status might be updated
    :param from_user: user object that initiated the request
    :param manager: boolean: if true, status of the user is active directly while if False, it is 'pending'
    :return: return status
    """
    manager_location_check = False
    # for i in location.location_managers.all():
    #     if i == user_to_update:
    #         manager_location_check = True
    if user_to_update in distrib.event_managers.all():
        manager_location_check = True
    if StatusUsersLocations.objects.filter(distrib=distrib, location=location, user=user_to_update):
        status = StatusUsersLocations.objects.filter(distrib=distrib, location=location, user=user_to_update).first()
        if status.status != 2 and (manager or manager_location_check):
            status.status = 2
            status.save()
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, user=user_to_update,
                                            from_user=from_user, status=2, current_status=status.status)
            logs.save()
        elif status.status == 2:
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, user=user_to_update, status=2,
                                            from_user=from_user, current_status=status.status)
            logs.save()

        elif status.status == 1 and not (manager or manager_location_check):
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, user=user_to_update, status=1,
                                            from_user=from_user, current_status=status.status)
            logs.save()

        else:
            status.status = 1
            status.save()
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, user=user_to_update, status=1,
                                            from_user=from_user, current_status=status.status)
            logs.save()
    else:
        if manager or manager_location_check:
            status = StatusUsersLocations(distrib=distrib, location=location, user=user_to_update, status=2)
            status.save()
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, user=user_to_update,
                                            from_user=from_user, status=2, current_status=status.status)
            logs.save()
        else:
            status = StatusUsersLocations(distrib=distrib, location=location, user=user_to_update)
            status.save()
            logs = LogsStatusUsersLocations(distrib=distrib, location=location, from_user=from_user,
                                            user=user_to_update, current_status=status.status)
            logs.save()
    return status


@login_required(login_url='/login/')
@admin_only
def location_create(request):
    form = LocationForm()
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            new_location = form.save()
            for i in new_location.location_managers.all():
                edit_user_type_to_manager(i)
                # check_if_new_status_to_create_update(location=new_location, user_to_update=i, from_user=request.user,
                #                                      manager=True)
            # edit_user_type_to_manager(new_location.manager_location)
            # check_if_new_status_to_create_update(location=new_location, user_to_update=new_location.manager_location, from_user=request.user, manager=True)
            return redirect('index')
    return render(request, 'location.html', context={"form": form})


@login_required(login_url='/login/')
@forbidden_to_user
def location_edit(request, location_id):
    location_page = Location.objects.get(uuid=location_id)
    form = LocationForm(instance=location_page)
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            location_page.name = form.cleaned_data['name']
            location_page.address = form.cleaned_data['address']
            location_page.address_2 = form.cleaned_data['address_2']
            location_page.city = form.cleaned_data['city']
            location_page.zip_code = form.cleaned_data['zip_code']
            location_page.country = form.cleaned_data['country']
            new_managers = form.cleaned_data['location_managers']
            current_managers = location_page.location_managers.all()
            for i in new_managers:
                if i not in current_managers:
                    location_page.location_managers.add(i)
                    edit_user_type_to_manager(i)
                    # check_if_new_status_to_create_update(location=location_page, user_to_update=i,
                    #                                      from_user=request.user, manager=True)

            for i in current_managers:
                if i not in new_managers and i not in [z.event_managers.all() for z in Event.objects.all()]:
                    location_page.location_managers.remove(i)
                    edit_user_type_to_user(i)
                    # check_if_new_status_to_create_update(location=location_page, user_to_update=i,
                    #                                      from_user=request.user)

            #     if location_page.manager_location != manager:
            #         edit_user_type_to_user(location_page.manager_location)
            #         location_page.manager_location = manager
            #         edit_user_type_to_manager(manager)
            #         check_if_new_status_to_create_update(location=location_page, user_to_update=manager, from_user=request.user, manager=True)
            location_page.save()
            # return redirect('index')
            return redirect(reverse('location_details', kwargs={'location_id': location_id}))
    return render(request, 'location.html', context={"form": form, 'is_edit': True, 'location_id': location_id})


@login_required(login_url='/login/')
def location_details(request, location_id):
    location_page = get_object_or_404(Location, uuid=location_id)
    message_form = MessagesEventsManagerDistrib()
    manager_location_check = False
    all_events_location = Event.objects.filter(location=location_page, is_distrib=True)
    for i in location_page.location_managers.all():
        if i == request.user:
            manager_location_check = True
    return render(request, 'location_details.html', context={"location": location_page,
                                                             "manager_location": manager_location_check,
                                                             "events": all_events_location, "message_form":message_form})


@login_required(login_url='/login/')
def locations(request):
    message_form = MessagesEventsSimpleForm()
    if request.user.user_type == 1:
        all_locations = Location.objects.all()
        return render(request, 'locations.html', context={"all_locations": all_locations, "admin": True, "message_form":message_form})
    elif Location.objects.filter(location_managers=request.user).count() == 0:
        return redirect('index')
    # elif Location.objects.filter(location_managers=request.user).count() == 1:
    #     return redirect(reverse('location_details', kwargs={
    #         'location_id': Location.objects.filter(location_managers=request.user).first().uuid}))
    elif request.user.user_type == 3:
        all_locations = Location.objects.filter(location_managers=request.user)
        return render(request, 'locations.html', context={"all_locations": all_locations, "message_form":message_form})
    else:
        return redirect('index')


@login_required(login_url='/login/')
def select_locations(request):
    # if StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(
    #         user=request.user, status=2):
    #     status_user_locations = StatusUsersLocations.objects.filter(user=request.user,
    #                                                                 status=1) | StatusUsersLocations.objects.filter(
    #         user=request.user, status=2)
    #     locations_user_status = [i.location.pk for i in status_user_locations]
    #     form = SelectLocationsForm(initial={'locations': locations_user_status})
    # else:
    #     form = SelectLocationsForm()

    if request.method == "POST":
        form = request.POST.getlist('distrib')
        events_from_form = []
        for i in form:
            event = get_object_or_404(Event, uuid=i)
            events_from_form.append(event)
            status_check = check_if_new_status_to_create_update(distrib=event,
                                                                location=Location.objects.get(uuid=event.location.uuid),
                                                                user_to_update=request.user, from_user=request.user,
                                                                manager=False)
            if status_check is not None and status_check.status == 1:
                try:
                    send_email(1, [event.event_managers.all()], request.user)
                except:
                    print('error - email send notif status location manager')
        for j in StatusUsersLocations.objects.filter(user=request.user).exclude(status=3).exclude(status=4).exclude(
                status=5):
            if j.distrib not in events_from_form:
                logs = LogsStatusUsersLocations(distrib=j.distrib, location=j.location, from_user=request.user,
                                                user=request.user, status=5, current_status=j.status)
                logs.save()
                if request.user in j.distrib.event_managers.all():
                    logs.is_at_time_event_manager = True
                    logs.save()
            # if (j.location not in locations_form and request.user.user_type != 1) and (j.location not in locations_form and j.location.manager_location != request.user):
            # manager_location_check = False
            # for z in j.location.location_managers.all():
            #     if request.user == z:
            #         manager_location_check = True
            if j.distrib not in events_from_form and request.user not in j.distrib.event_managers.all():
                j.status = 5
                j.save()
                for i in AttendeesEvents.objects.filter(parent_event=j.distrib, user=request.user):
                    if datetime(i.event_date.year, i.event_date.month, i.event_date.day) > datetime.now():
                        i.delete()
        return redirect('index')

    # form = SelectLocationsForm(data=request.POST)
    # if form.is_valid():
    #     locations_form = form.cleaned_data['locations']
    #     for i in locations_form:
    #         status_check = check_if_new_status_to_create_update(location=i, user_to_update=request.user, from_user=request.user, manager=False)
    #         if status_check is not None and status_check.status == 1:
    #             try:
    #                 send_email(request.user, i.location_managers.first().email)
    #             except:
    #                 print('error - email send notif status location manager')
    #     for j in StatusUsersLocations.objects.filter(user=request.user).exclude(status=3).exclude(status=4).exclude(status=5):
    #         if j.location not in locations_form:
    #             logs = LogsStatusUsersLocations(location=j.location, from_user=request.user, user=request.user, status=5,
    #                                      current_status=j.status)
    #             logs.save()
    #         # if (j.location not in locations_form and request.user.user_type != 1) and (j.location not in locations_form and j.location.manager_location != request.user):
    #         manager_location_check = False
    #         for z in j.location.location_managers.all():
    #             if request.user == z:
    #                 manager_location_check = True
    #         if j.location not in locations_form and not manager_location_check:
    #             j.status =5
    #             j.save()
    # return redirect('index')

    event_form_locations = Event.objects.filter(is_distrib=True, is_cancelled=False)
    all_locations = Location.objects.all()
    return render(request, 'select_locations.html', context={"event_form_locations": event_form_locations,
                                                             "all_locations": all_locations})



