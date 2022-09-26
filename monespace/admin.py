from django.contrib import admin

from .models import User, Location, Event, RecurringPattern, StatusUsersLocations, LogsStatusUsersLocations, \
    EventExceptionCancelledRescheduled, AttendeesEvents, Message, MessageSeen


class UserAdminCustom(admin.ModelAdmin):
    list_display = ('uuid', "username", 'email', 'user_type', 'date_joined')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('uuid', "name", "address", "address_2", "city", "zip_code", "country", 'created')


class EventAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'location', 'name', 'start_date', 'is_recurring', 'is_distrib', 'is_cancelled', 'created')


class RecurringPatternAdmin(admin.ModelAdmin):
    list_display = ('event', "separation_count", "max_num_occurrences", 'created')


class StatusUsersLocationsAdmin(admin.ModelAdmin):
    list_display = ("uuid", 'location', 'distrib',  "user", 'status', 'created', 'modified')


class LogsStatusUsersLocationsAdmin(admin.ModelAdmin):
    list_display = ('location', 'distrib', 'from_user', "user", 'status', 'current_status', 'created')


class EventExceptionCancelledRescheduledAdmin(admin.ModelAdmin):
    list_display=('location', 'parent_event', 'start_date', 'is_cancelled', 'is_rescheduled')


class AttendeesEventsAdmin(admin.ModelAdmin):
    list_display = ('parent_event', 'user', 'status', 'event_date', 'plus_other')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('uuid', "from_user", 'to_location', "to_event", "to_event_manager_group", "to_event_date", "to_event_group", "to_user", "info_all_locations")


class MessageSeenAdmin(admin.ModelAdmin):
    list_display = ( "user", 'message', "date_seen")


admin.site.register(User, UserAdminCustom)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringPattern, RecurringPatternAdmin)
admin.site.register(StatusUsersLocations, StatusUsersLocationsAdmin)
admin.site.register(LogsStatusUsersLocations, LogsStatusUsersLocationsAdmin)
admin.site.register(EventExceptionCancelledRescheduled, EventExceptionCancelledRescheduledAdmin)
admin.site.register(AttendeesEvents, AttendeesEventsAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageSeen, MessageSeenAdmin)
