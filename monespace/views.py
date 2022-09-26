from pprint import pprint

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

from .models import Location, StatusUsersLocations, LogsStatusUsersLocations, User, AttendeesEvents, Event
from .views_events import events_list
from .forms import StatusUsersLocationsForm, UserProfileForm, MessagesEventsForm, MessagesEventsSimpleForm
from .functions_global import get_date_to, forbidden_to_user, admin_only
from .views_messages import get_to_user_messages, get_from_user_messages


@login_required(login_url='/login/')
def index(request):

    to_user_messages = get_to_user_messages(request.user)
    from_user_messages = get_from_user_messages(request.user)

    user_distrib_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | \
                         StatusUsersLocations.objects.filter(user=request.user, status=2)
    distrib_user_choice = [i.distrib for i in user_distrib_pre if not i.distrib.is_cancelled]
    distrib_attendees = [i.parent_event for i in AttendeesEvents.objects.filter(user=request.user)]
    distrib = [i for i in distrib_user_choice]
    for i in distrib_attendees:
        if i not in distrib and not i.is_cancelled:
            distrib.append(i)

    if StatusUsersLocations.objects.filter(user=request.user, status=1):
        pending_events = StatusUsersLocations.objects.filter(user=request.user, status=1)
    else:
        pending_events = None

    events_user_manager = [i for i in Event.objects.all() if request.user in i.event_managers.all()]
    pending_approval_in_events = StatusUsersLocations.objects.filter(status=1, distrib__in=events_user_manager)
    if len(pending_approval_in_events) > 0:
        users_to_approve = True
        distrib_users_to_approve = pending_approval_in_events[0].distrib.uuid
    else:
        users_to_approve = False
        distrib_users_to_approve = None

    attendees = AttendeesEvents.objects.filter(user=request.user)

    eligible_events_date_locations_attendees_final = events_list(date_from=None, date_to=None, location=None, distrib=None, event_manager=None, attendance=True, user_requester=request.user)

    date_to = datetime.datetime.now() - datetime.timedelta(days=1) + datetime.timedelta(weeks=8)
    events_manager = events_list(date_from=None, date_to=date_to, location=None, event_manager=request.user, distrib=None)
    message_form = MessagesEventsForm()
    return render(request, 'index.html', context={"events": eligible_events_date_locations_attendees_final,
                                                  "date_to": date_to, "pending_events":pending_events,
                                                  "attendees": attendees, "events_manager": events_manager,
                                                  "message_form": message_form, "to_user_messages": to_user_messages,
                                                  "from_user_messages": from_user_messages,
                                                  "users_to_approve":users_to_approve,
                                                  "distrib_users_to_approve":distrib_users_to_approve})


def faq_view(request):
    return render(request, 'faq.html')


@login_required(login_url='/login/')
@admin_only
def all_users_site(request):
    users = User.objects.all().order_by('first_name')
    form = StatusUsersLocationsForm()
    message_form = MessagesEventsSimpleForm()
    status_users_location = StatusUsersLocations.objects.all().order_by('user__first_name')
    # status_users_location = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    return render(request, 'benevoles.html', context={"status_users_location": status_users_location, "form": form, "users":users, "message_form":message_form})


@login_required(login_url='/login/')
@forbidden_to_user
def users_site(request, location_id):
    if request.user.user_type == 3 and Location.objects.get(uuid=location_id) not in Location.objects.filter(location_managers=request.user):
        return redirect('index')
    else:
        status_users_location = StatusUsersLocations.objects.filter(location=Location.objects.get(uuid=location_id),
                                                                    status=1) | StatusUsersLocations.objects.filter(
            location=Location.objects.get(uuid=location_id), status=2)
        users_pre = [i.user for i in status_users_location.order_by('user__first_name')]
        users=[]
        for i in users_pre:
            if i not in users:
                users.append(i)

        form = StatusUsersLocationsForm()
        message_form = MessagesEventsSimpleForm()

        if request.method == "POST":
            try:
                user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
            except:
                pass
            else:
                user_status_update.status = 2
                user_status_update.save()
                logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=2, current_status=user_status_update.status)
                logs.save()
                return redirect(reverse('users_site', kwargs={'location_id': location_id}))
        return render(request, 'benevoles_site.html', context={'location_id': location_id, "status_users_location": status_users_location, "form": form, "users":users, "message_form":message_form})


@login_required(login_url='/login/')
@forbidden_to_user
def user_site_update_status(request, location_id):
    if request.method == "POST":
        try:
            user_status_update = StatusUsersLocations.objects.get(uuid=request.GET['id'])
        except:
            pass
        else:
            user_status_update.status = request.POST['status']
            user_status_update.save()
            logs = LogsStatusUsersLocations(location=user_status_update.location, from_user=request.user, user=user_status_update.user, status=request.POST['status'], current_status=user_status_update.status)
            logs.save()
            return redirect(reverse('users_site', kwargs={'location_id': location_id}))
    return redirect('index')


@login_required(login_url='/login/')
def profile(request):
    message_form = MessagesEventsSimpleForm()
    date_to = get_date_to()
    user_distrib_pre = StatusUsersLocations.objects.filter(user=request.user, status=1) | StatusUsersLocations.objects.filter(user=request.user, status=2)
    user_distrib = [i for i in user_distrib_pre if not i.distrib.is_cancelled]
    # user_locations = [i.location for i in user_locations_pre]
    user_manager_locations = Location.objects.filter(location_managers=request.user)
    return render(request, 'profile.html', context={'distrib': user_distrib, "date_to":date_to,
                                                    'manager_locations': user_manager_locations,"message_form":message_form })



@login_required(login_url='/login/')
def profile_edit(request):
    form = UserProfileForm(instance=request.user)
    if request.method == "POST":
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            updated_user = request.user
            try:
                image = request.FILES['profile_picture']
            except:
                pass
            else:
                request.user.save_image(image)
            finally:
                updated_user.first_name = form.cleaned_data['first_name']
                updated_user.last_name = form.cleaned_data['last_name']
                updated_user.email = form.cleaned_data['email']
                updated_user.address = form.cleaned_data['address']
                updated_user.city = form.cleaned_data['city']
                updated_user.zip_code = form.cleaned_data['zip_code']
                updated_user.tel = form.cleaned_data['tel']
                updated_user.save()
                return redirect('profile')
    return render(request, 'profile_edit.html', context={"form" : form})


@login_required(login_url='/login/')
@forbidden_to_user
def profile_edit_manager(request, user_id, distrib_id):
    distrib = get_object_or_404(Event, uuid=distrib_id)
    if request.user.user_type == 3 and Location.objects.get(uuid=distrib.location.uuid) not in Location.objects.filter(location_managers=request.user):
        return redirect('index')
    else:
        updated_user = get_object_or_404(User, uuid=user_id)
        form = UserProfileForm(instance=updated_user)
        if request.method == "POST":
            form = UserProfileForm(data=request.POST)
            if form.is_valid():
                try:
                    image = request.FILES['profile_picture']
                except:
                    pass
                else:
                    request.user.save_image(image)
                finally:
                    updated_user.first_name = form.cleaned_data['first_name']
                    updated_user.last_name = form.cleaned_data['last_name']
                    updated_user.email = form.cleaned_data['email']
                    updated_user.address = form.cleaned_data['address']
                    updated_user.city = form.cleaned_data['city']
                    updated_user.zip_code = form.cleaned_data['zip_code']
                    updated_user.tel = form.cleaned_data['tel']
                    updated_user.save()
                    return redirect(reverse('distrib_users', kwargs={'distrib_id': distrib_id}))
        return render(request, 'profile_edit_manager.html', context={"form" : form, "distrib":distrib, "user":updated_user})


@login_required(login_url='/login/')
@admin_only
def profile_edit_admin(request, user_id):
    updated_user = get_object_or_404(User, uuid=user_id)
    form = UserProfileForm(instance=updated_user)
    if request.method == "POST":
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            try:
                image = request.FILES['profile_picture']
            except:
                pass
            else:
                request.user.save_image(image)
            finally:
                updated_user.first_name = form.cleaned_data['first_name']
                updated_user.last_name = form.cleaned_data['last_name']
                updated_user.email = form.cleaned_data['email']
                updated_user.address = form.cleaned_data['address']
                updated_user.city = form.cleaned_data['city']
                updated_user.zip_code = form.cleaned_data['zip_code']
                updated_user.tel = form.cleaned_data['tel']
                updated_user.save()
                return redirect(reverse('all_users_site'))
    return render(request, 'profile_edit_admin.html', context={"form": form, "user": updated_user})
