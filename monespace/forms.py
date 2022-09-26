from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Event, Location, RecurringPattern, StatusUsersLocations, AttendeesEvents, Message


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", 'last_name', "email", "address", "city", "zip_code", "tel", "profile_picture")
        widgets = {
            "profile_picture": forms.FileInput(),
            "first_name": forms.TextInput(attrs={'required': 'true'}),
            "last_name": forms.TextInput(attrs={'required': 'true'}),
            "email":forms.EmailInput(attrs={'required': 'true'}),
        }
        labels = {
            "first_name": "Prénom *",
            'last_name': "Nom *",
            "email": "Email *",
            "address": "Adresse",
            "city":"Ville",
            "zip_code": "Code Postal",
            "tel":"Téléphone pour vous joindre",
            "profile_picture": "Photo de profil"
        }


class UserAuthenticationForm(AuthenticationForm):
    pass


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('location', "name", "description", "start_date", "end_date", "is_full_day", "time_from", "time_to", "is_recurring", "event_managers")
        widgets = {
            "start_date":forms.DateInput(attrs={'type': 'date'}),
            "end_date": forms.DateInput(attrs={'type': 'date'}),
            "time_from": forms.TimeInput(attrs={'type': 'time'}),
            "time_to": forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            "location": "Site de l'événement",
            "name": "Nom de l'événement",
            "description": "Description",
            "start_date": "Date de début",
            "end_date": "Date de fin",
                "time_from": "Heure de début",
                    "time_to": "Heure de fin",
                    "is_full_day": "L'événement dure toute la journée",
            "is_recurring": "L'événement se répète",
            "event_managers": "Responsables de l'événement"
        }


class DistributionForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "start_date", "time_from", "time_to", "event_managers")
        widgets = {
            "start_date": forms.DateInput(attrs={'type': 'date'}),
            "time_from": forms.TimeInput(attrs={'type': 'time'}),
            "time_to": forms.TimeInput(attrs={'type': 'time'}),
            "event_managers": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "name": "Nom de la soirée de distribution *",
            "start_date": "Date de début *",
            "time_from": "Heure de début *",
            "time_to": "Heure de fin *",
            "event_managers": "Responsables de la soirée distribution *"
        }


class DistributionManagerForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("time_from", "time_to", "event_managers", "pre_alert_non_attendees_status", "pre_alert_non_attendees_nb_attendees")
        labels = {
            "time_from": "Heure de début *",
            "time_to": "Heure de fin *",
            "event_managers": "Modifier les responsables de la soirée de distribution",
            "pre_alert_non_attendees_status": "Voulez vous activer une alerte automatique envoyée 2 jours avant l'événement si le nombre de bénévoles est inférieur au nombre désiré ?",
            "pre_alert_non_attendees_nb_attendees": "En dessous de ce nombre, l'alerte, si active sera envoyée"
        }
        widgets = {
            "time_from": forms.TimeInput(attrs={'type': 'time'}),
            "time_to": forms.TimeInput(attrs={'type': 'time'}),
            "event_managers": forms.CheckboxSelectMultiple(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(DistributionManagerForm, self).__init__(*args, **kwargs)
    #     managers = [(i.uuid, i) for i in User.objects.all()]
    #     self.fields['event_manager'] = forms.ChoiceField(choices=managers)
    #     self.fields["event_manager"].label = "Séléctionner le nouveau responsable de la soirée distribution"


class EventRecurringPatternForm(forms.ModelForm):
    class Meta:
        model = RecurringPattern
        repeat_each_x_choices = ((0, 'semaine'), (1, 'jour'), (2, 'mois'), (3, 'trimestre'),
                                (4, 'semestre'), (5, 'année'))
        day_of_week_choices = ((0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'), (4, 'Vendredi'),
                               (5, 'Samedi'), (6, 'Dimanche'))

        fields = ('separation_count', "repeat_each_x", "max_num_occurrences")
        widgets = {
            "day_of_week": forms.RadioSelect(choices=day_of_week_choices),
            "repeat_each_x": forms.Select(choices=repeat_each_x_choices),
        }

        labels = {
            "day_of_week": "le",
            'separation_count': 'répéter tous/toutes les',
            'repeat_each_x': '',
            "max_num_occurrences": "pendant... fois (en plus de celui ci)"
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        # fields = '__all__'
        fields = ("name", "address", "address_2", "city", "zip_code", "country", "location_managers")
        labels = {
            "name": "Nom du site *",
            "address": "Adresse *",
            "address_2": "Complément d'adresse",
            "city": "Ville *",
            "zip_code": "Code postal *",
                    "country": "Pays",
            "location_managers": "Gestionnaires du site *"
        }
        widgets = {
            "location_managers": forms.CheckboxSelectMultiple(),
        }


class SelectLocationsForm(forms.Form):
    locations = forms.ModelMultipleChoiceField(Location.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)


class StatusUsersLocationsForm(forms.ModelForm):
    class Meta:
        model = StatusUsersLocations
        fields = ('status',)


class AttendeesEventsForm(forms.ModelForm):
    class Meta:
        model = AttendeesEvents
        fields = ('plus_other',)


class MessagesEventsForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('to_event_group', "subject", 'description')
        widgets = {
            "to_event_group": forms.Select(attrs={'required': 'true'}),
        }
        labels = {
            "to_event_group": "Séléctionner à qui envoyer ce message *",
            "subject" : "Sujet de votre message *",
            "description": "Votre message"
        }


class MessagesEventsSimpleForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", 'description')
        labels = {
            "subject": "Sujet de votre message *",
            "description": "Votre message"
        }


class MessagesEventsManagerDistrib(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('to_event_manager_group', "subject",'description')
        labels = {
            "to_event_manager_group": "Séléctionner à qui envoyer ce message *",
            "subject": "Sujet de votre message *",
            "description": "Votre message"
        }