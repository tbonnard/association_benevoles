from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .models import Event, AttendeesEvents, RecurringPattern


@login_required(login_url='/login/')
def api_get_all_attendees_user(request):
    attendees = AttendeesEvents.objects.filter(user=request.user)
    return JsonResponse([i.serialize() for i in attendees], safe=False)


@login_required(login_url='/login/')
def api_attend_decline_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        attendee_type = data.get('type')
        event = Event.objects.get(uuid=data.get('parent_event'))
        date = data.get('event_date')
        if event.is_recurring:
            rec_pattern = RecurringPattern.objects.filter(event=event).first()
        else:
            rec_pattern = None
        if attendee_type == "attend":
            new_attendee = AttendeesEvents(user=request.user, parent_event=event, event_date=date,
                                           recurring_pattern=rec_pattern, time_from=event.time_from, time_to=event.time_to)
            new_attendee.save()
            return JsonResponse({"message": 'OK'}, status=201)
        elif attendee_type == "decline":
            attend_decline = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
            attend_decline.delete()
            return JsonResponse({"message": 'OK'}, status=201)
        elif attendee_type == "plus_other":
            attend_to_update = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date).first()
            attend_to_update.plus_other = data.get('plus_other')
            attend_to_update.save()
            return JsonResponse({"message": 'OK'}, status=201)
        else:
            return JsonResponse({"error": "try again - not found - api_attend_decline_event"}, status=400)
    return JsonResponse({"error": "try again - not a POST - api_attend_decline_event"}, status=400)


@login_required(login_url='/login/')
def api_get_specific_attendees(request):
    event = Event.objects.get(uuid=request.GET['parent_event'])
    date = request.GET['event_date']
    attendees = AttendeesEvents.objects.filter(user=request.user, parent_event=event, event_date=date)
    return JsonResponse([i.serialize() for i in attendees], safe=False)


def get_count_event_specific(event, date):
    all_attendees = AttendeesEvents.objects.filter(parent_event=event, event_date=date)
    count_attendees = 0
    if len(all_attendees) > 0:
        count_attendees = all_attendees.count()
        for i in all_attendees:
            count_attendees += i.plus_other
    return count_attendees


@login_required(login_url='/login/')
def api_get_count_specific_attendees(request):
    data = json.loads(request.body)
    parent_event = data.get('parent_event')
    date = data.get('event_date')
    try:
        event = Event.objects.get(uuid=parent_event)
    except:
        return JsonResponse({"error": "try again - not found - api_get_count_specific_attendees"}, status=400)
    else:
        count_attendees = get_count_event_specific(event, date)
        return JsonResponse([count_attendees], safe=False)