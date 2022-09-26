import datetime
from functools import wraps
from django.shortcuts import redirect

from .models import Event


def get_date_to():
    weeks = 8
    days_added = datetime.timedelta(weeks=weeks)
    date_to = (datetime.datetime.now() + days_added).strftime("%Y-%m-%d")
    return date_to


def forbidden_to_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if args[0].user.user_type == 2:
            print("no access - forbidden to user")
            return redirect('index')
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if args[0].user.user_type != 1:
            print("no access - admin only")
            return redirect('index')
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def location_manager_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print(args[0])
        # print(kwargs['event_id'])
        try:
            event = Event.objects.get(uuid=kwargs['event_id'])
        except:
            print("event not found")
            return redirect('index')
        else:
            manager_location_check = False
            for i in event.location.location_managers.all():
                if i == args[0].user:
                    manager_location_check = True
            if not manager_location_check and args[0].user.user_type !=1:
                print("no access - not manager")
                return redirect('index')
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function