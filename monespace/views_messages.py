import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Event, Location, Message, User, StatusUsersLocations, AttendeesEvents, MessageSeen
from .notification_manager import send_email


@login_required(login_url='/login/')
def send_message(request):
    data = json.loads(request.body)
    date = data.get('date')
    all_site = data.get('all_site')
    group = data.get('group')
    description = data.get('description')
    user_uuid = data.get('user')
    subject = data.get('subject')
    group_manager = data.get('groupManager')


    try:
        users_to = User.objects.get(uuid=user_uuid)
    except:
        users_to = None

    event_uuid = data.get('event')
    try:
        event = Event.objects.get(uuid=event_uuid)
    except:
        event = None
    site_uuid = data.get('site')
    try:
        location = Location.objects.get(uuid=site_uuid)
    except:
        location = None

    new_message = Message(subject=subject, to_event=event, to_location=location, from_user=request.user,
                          to_event_group=group, description=description, info_all_locations=all_site,
                          to_event_date=date, to_user=users_to, to_event_manager_group=group_manager)
    new_message.save()
    group_message = int(new_message.to_event_group)

    users_to = []
    # print('start')
    if new_message.to_user is not None:
        # print('user')
        users_to.append(new_message.to_user)
    elif new_message.to_event_date is not None:
        # print('a')
        if group_message == 2:
            # print('2a')
            for i in AttendeesEvents.objects.filter(parent_event=new_message.to_event, event_date=new_message.to_event_date, status=1):
                # print('attendee')
                users_to.append(i.user)
        elif group_message == 3:
            # print('b')
            attendees = AttendeesEvents.objects.filter(parent_event=new_message.to_event, event_date=new_message.to_event_date, status=1)
            attendees_user = [i.user for i in attendees]
            # print('3 start')
            for i in StatusUsersLocations.objects.filter(distrib=new_message.to_event, status=2):
                if i.user not in attendees_user:
                    # print('non attendee')
                    users_to.append(i.user)
        else:
            # print('c')
            for i in StatusUsersLocations.objects.filter(distrib=new_message.to_event, status=2):
                # print('all att or non att de distirb')
                users_to.append(i.user)
    elif new_message.to_event is not None and new_message.to_event_date is None:
        # print('d')
        if new_message.to_event_manager_group == 1:
            for i in Event.objects.filter(id=new_message.to_event.id).event_managers.all():
                users_to.append(i)
        else:
            for i in StatusUsersLocations.objects.filter(distrib=new_message.to_event, status=2):
                # print('all de distirb')
                users_to.append(i.user)
    elif new_message.to_location is not None:
        # print('e')
        for i in StatusUsersLocations.objects.filter(location=new_message.to_location, status=2):
            # print('all de location')
            users_to.append(i.user)
    elif new_message.all_site:
        # print('f')
        for i in StatusUsersLocations.objects.filter(status=2):
            # print('all de all')
            users_to.append(i.user)
    else:
        pass
        # print('nothing')
    users_to_final = tuple(users_to)
    # send message
    send_email(2, users_to_final, request.user, message_desc=new_message.description)

    return JsonResponse({"Success": "Le message a été créé"}, status=200)


def get_to_user_messages(user):
    to_user_events_pre = StatusUsersLocations.objects.filter(user=user, status=2)
    all_to_user_events = [i.distrib for i in to_user_events_pre]
    if user.user_type != 2:
        ditrib_managers = [i for i in Event.objects.all() if user in i.event_managers.all()]
        for i in ditrib_managers:
            all_to_user_events.append(i)
    messages_events = Message.objects.filter(to_event__in=all_to_user_events)
    # all_attend_to_user_events = []
    # attend_to_user_events = []
    # non_attend_to_user_events = []

    to_user_events_groups = []
    for i in messages_events:
        if i.to_event_manager_group == 1:
            if user in i.to_event.event_managers.all():
                to_user_events_groups.append(i.id)
        elif i.to_event_group == 1 and i.created >= user.date_joined:
            # all_attend_to_user_events.append(i)
            to_user_events_groups.append(i.id)
        elif i.to_event_group == 2:
            if AttendeesEvents.objects.filter(user=user, parent_event=i.to_event, event_date=i.to_event_date):
                # attend_to_user_events.append(i)
                to_user_events_groups.append(i.id)
        elif i.to_event_group == 3:
            if not AttendeesEvents.objects.filter(user=user, parent_event=i.to_event, event_date=i.to_event_date) and i.created >= user.date_joined:
                # non_attend_to_user_events.append(i)
                to_user_events_groups.append(i.id)

    to_user_distrib = []
    for i in messages_events:
        if i.to_event_group is None and i.created >= user.date_joined:
            to_user_distrib.append(i)

    to_user_locations_pre = StatusUsersLocations.objects.filter(user=user, status=2)
    to_user_locations = [i.location for i in to_user_locations_pre]

    to_user_messages = Message.objects.filter(to_user=user) | Message.objects.filter(id__in=to_user_events_groups) \
                       | Message.objects.filter(to_location__in=to_user_locations, created__gte=user.date_joined) \
                       | Message.objects.filter(info_all_locations=True, created__gte=user.date_joined)
    to_user_messages_tuple = tuple(to_user_messages.order_by('-created'))
    return to_user_messages_tuple


def get_from_user_messages(user):
    from_user_messages = Message.objects.filter(from_user=user)
    return from_user_messages.order_by('-created')


@login_required(login_url='/login/')
def get_info_if_new_messages(request):
    messages = get_to_user_messages(request.user)
    messages_seen = [i.message for i in MessageSeen.objects.filter(user=request.user)]
    new_message = []
    for i in messages:
        if i not in messages_seen:
            new_message.append(i)
    return JsonResponse([i.serialize() for i in new_message], safe=False)


def get_messages_seen(user):
    messages = get_to_user_messages(user)
    messages_seen = [i.message for i in MessageSeen.objects.filter(user=user)]
    new_message = []
    for i in messages:
        if i not in messages_seen:
            new_message.append(i)
    return new_message


@login_required(login_url='/login/')
def create_messages_seen(request):
    if request.method == 'POST':
        user = request.user
        messages = get_messages_seen(user)
        for i in messages:
            if not MessageSeen.objects.filter(user=user, message=i):
                new_seen = MessageSeen(user=user, message=i)
                new_seen.save()
        return JsonResponse(True, safe=False)


@login_required(login_url='/login/')
def create_message_seen(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            message = Message.objects.get(uuid=data.get('message'))
        except:
            return JsonResponse(False, safe=False)
        user = request.user
        if not MessageSeen.objects.filter(user=user, message=message):
            new_seen = MessageSeen(user=user, message=message)
            new_seen.save()
        return JsonResponse(True, safe=False)
