from django.urls import path
from . import views, views_login, views_events, views_locations, views_download, views_attend, views_distrib, views_messages
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views_login.login_view, name='login_view'),
    path('login_admin/', views_login.login_view_admin, name='login_view_admin'),
    path('register/', views_login.register, name='register'),
    path('logout/', views_login.logout_view, name='logout_view'),
    path('faq/', views.faq_view, name='faq'),
    path('profil/', views.profile, name='profile'),
    path('profil/modifier/', views.profile_edit, name='profile_edit'),
    path('profil/modifier/<uuid:user_id>/<uuid:distrib_id>/', views.profile_edit_manager, name='profile_edit_manager'),
    path('profil/modifier/<uuid:user_id>/', views.profile_edit_admin, name='profile_edit_admin'),
    path('site/benevoles/<uuid:location_id>/', views.users_site, name='users_site'),
    path('benevoles/', views.all_users_site, name='all_users_site'),
    path('benevoles_status/<uuid:location_id>/', views.user_site_update_status, name='user_site_update_status'),
    path('benevoles_distrib_status/<uuid:distrib_id>/', views_distrib.user_distrib_update_status, name='user_distrib_update_status'),
    path('distribution/liste/', views_distrib.distributions, name='distributions'),
    path('distribution/benevoles/<uuid:distrib_id>/', views_distrib.distrib_users, name='distrib_users'),
    path('distribution/creer/<uuid:location_id>/', views_distrib.distribution_create, name='distribution_create'),
    path('distribution/details/<uuid:distrib_id>/', views_distrib.distrib_details, name='distrib_details'),
    path('distribution/modifier_responsable/<uuid:distrib_id>/', views_distrib.change_distrib_manager, name='change_distrib_manager'),
    path('get_event_location/', views_distrib.get_event_location, name='get_event_location'),
    path('get_user_distrib/', views_distrib.get_user_distrib, name='get_user_distrib'),
    path('get_count_event_location/<uuid:location_id>/', views_distrib.get_count_event_location,name='get_count_event_location'),
    path('get_count_event_benev/', views_distrib.get_count_event_benev, name='get_count_event_benev'),
    path('event/creer/', views_events.event_create, name='event_create'),
    path('event/details/<uuid:event_id>/', views_events.event_details, name='event_details'),
    path('event/modifier/<uuid:event_id>/', views_events.event_edit, name='event_edit'),
    path('event/modifier/simple/<uuid:event_id>/', views_events.event_edit_specific_rec, name='event_edit_specific_rec'),
    path('event/liste/', views_events.events_list_date, name='events_list_date'),
    path('event_delete_all/<uuid:event_id>/', views_events.event_delete_all, name='event_delete_all'),
    path('event_delete_rec/<uuid:event_id>/', views_events.event_delete_rec, name='event_delete_rec'),
    path('reactivate_event_date/<uuid:event_id>/', views_events.reactivate_event_date, name='reactivate_event_date'),
    path('site/creer/', views_locations.location_create, name='location_create'),
    path('site/liste', views_locations.locations, name='locations'),
    path('profil/selectionner_sites/', views_locations.select_locations, name='select_locations'),
    path('site/<uuid:location_id>/', views_locations.location_details, name='location_details'),
    path('site/modifier/<uuid:location_id>/', views_locations.location_edit, name='location_edit'),
    path('download_users_csv/', views_download.download_users_csv, name='download_users_csv'),
    path('download_users_csv_distrib/', views_download.download_users_csv_distrib, name='download_users_csv_distrib'),
    path('api_get_specific_attendees/', views_attend.api_get_specific_attendees, name='api_get_specific_attendees'),
    path('api_get_count_specific_attendees/', views_attend.api_get_count_specific_attendees, name='api_get_count_specific_attendees'),
    path('api_get_all_attendees_user/', views_attend.api_get_all_attendees_user, name='api_get_all_attendees_user'),
    path('api_attend_decline_event/', views_attend.api_attend_decline_event, name='api_attend_decline_event'),
    path('events_list_json/<uuid:user_id>/', views_events.events_list_json, name='events_list_json'),
    path('send_message/', views_messages.send_message, name='send_message'),
    path('get_info_if_new_messages/', views_messages.get_info_if_new_messages, name='get_info_if_new_messages'),
    path('create_messages_seen/', views_messages.create_messages_seen, name='create_messages_seen'),
    path('create_message_seen/', views_messages.create_message_seen, name='create_message_seen'),

    # Change Password
    path('profil/changer-mot-de-passe/', auth_views.PasswordChangeView.as_view(
            template_name='commons/change_password.html',
            success_url='/'
        ), name='change_password'),

    # Forget Password
    path('password-reset/', auth_views.PasswordResetView.as_view(
             template_name='commons/password_reset/password_reset.html',
             subject_template_name='commons/password_reset/password_reset_subject.txt',
             email_template_name='commons/password_reset/password_reset_email.html',
             # success_url='/login/'
         ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password_reset/password_reset_done.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password_reset/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/',  auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password_reset/password_reset_complete.html'
         ), name='password_reset_complete'),

]

