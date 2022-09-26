import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import StatusUsersLocations, Location, Event
from .functions_global import forbidden_to_user


@login_required(login_url='/login/')
@forbidden_to_user
def download_users_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="monespace_benevoles.csv"'},
    )

    writer = csv.writer(response)
    all_users=[]

    try:
        request.GET['site']
        location = Location.objects.get(uuid=request.GET['site'])
    except:
        all_users = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    else:
        if location in Location.objects.filter(location_managers=request.user):
            all_users = StatusUsersLocations.objects.filter(status=1, location=location) | StatusUsersLocations.objects.filter(status=2, location=location)
        else:
            return redirect('index')
    finally:
        writer.writerow(['Nom utilisateur', 'Email', 'Prénom', 'Nom', 'Site', 'Soirée de distribution', 'Status dans cette distribution', 'Adresse du bénévole', 'Ville du bénévole', "Code postal du bénévole", "Téléphone du bénévole"])
        for i in all_users:
                writer.writerow([i.user.username, i.user.email, i.user.first_name , i.user.last_name, i.location.name, i.distrib.name, i.get_status_display(), i.user.address, i.user.city, i.user.zip_code, i.user.tel])

    return response


@login_required(login_url='/login/')
@forbidden_to_user
def download_users_csv_distrib(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="monespace_benevoles.csv"'},
    )

    writer = csv.writer(response)
    all_users=[]

    try:
        request.GET['distrib']
        distrib = Event.objects.get(uuid=request.GET['distrib'])
    except:
        return redirect('index')
    else:
        all_users = StatusUsersLocations.objects.filter(status=1,
                                                        distrib=distrib) | StatusUsersLocations.objects.filter(status=2,
                                                                                                               distrib=distrib)

        # if distrib.event_manager == request.user or request.user.user_type == 1:
        #     all_users = StatusUsersLocations.objects.filter(status=1, distrib=distrib) | StatusUsersLocations.objects.filter(status=2, distrib=distrib)
        # else:
        #     return redirect('index')
    finally:
        writer.writerow(['Nom utilisateur', 'Email', 'Prénom', 'Nom', 'Site', 'Soirée de distribution', 'Status dans cette distribution', 'Adresse du bénévole', 'Ville du bénévole', "Code postal du bénévole", "Téléphone du bénévole"])
        for i in all_users:
                writer.writerow([i.user.username, i.user.email, i.user.first_name , i.user.last_name, i.location.name, i.distrib.name, i.get_status_display(), i.user.address, i.user.city, i.user.zip_code, i.user.tel])

    return response

