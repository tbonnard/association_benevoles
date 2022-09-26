import smtplib
import os
import environ
from django.core.mail import send_mail, send_mass_mail

env = environ.Env()
# reading .env file
environ.Env.read_env()

email_gmail = env("email_gmail")
pwd_gmail = env("pwd_gmail")


def send_email(type_email, to_user, from_user, **kwargs):
    if from_user is None:
        from_user = email_gmail
    # print(to_user)
    if type_email == 1:
        subject = f"Approbation d'un nouveau bénévole"
        message_body = f"Un bénévole a demandé à être bénévole dans votre site. Merci d'approuver ou non cet utilisateur depuis la plateforme."
    elif type_email == 2:
        subject = f"Nouveau message de {from_user.first_name} pour vous sur la plateforme des bénévoles"
        message_body = f"Vous venez de recevoir un nouveau message. Voici le message de {from_user.first_name}: {kwargs['message_desc']}."
    elif type_email == 3:
        subject = f"Votre approbation pour rejoindre la distribution a été acceptée"
        message_body = f"Vous venez d'être approuvé par le responsable de distribution à rejoindre '{kwargs['distrib']}' . Vous pouvez maintenant vous rendre sur la plateforme et indiquer vos présences / voir les communications."
    elif type_email == 4:
        subject = f"Votre demande pour rejoindre la distribution a été refusée"
        message_body = f"Votre demande de rejoindre '{kwargs['distrib']}' a été refusée. Si vous pensez que cela pourrait être une erreur, merci de communiquer avec nous."
    elif type_email == 5:
        subject = f"Une distribution dans 1 journée!"
        message_body = f"Ceci est un rappel que vous êtes présent à une distribution dans 2 jours (le {kwargs['date']}). Merci de modifier votre présence si jamais vous ne pouvez malheureusement plus venir."
    elif type_email == 6:
        subject = f"La distribution du {kwargs['date']} vient d'être annuleé"
        message_body = f"La distribution '{kwargs['distrib']}' a été annulée pour la date du {kwargs['date']}"
    elif type_email == 7:
        subject = f"Bienvenue parmi nous!"
        message_body = f"C'est un reéel plaisir de vous compter parmi nous! Maintenant que vous être inscrit, séléctionner les distributions our lesquels vous souhaitez être membre et compléter votre profil pour faciliter la vie du gestionnaire de distribution! Nous vous remercions infiniment et avons hàte te de vous voir!"
    elif type_email == 8:
        subject = f"Seriez vous disponible dans 2 jours ?"
        message_body = f"La distribution '{kwargs['distrib']}' qui tiendra lieu dans 2 jours (le {kwargs['date']}) manque de bénévoles. Si vous êtes disponible, merci de marquer votre présence sur la plateforme! Merci beaucoup."
    else:
        subject = 'Notification de la plateforme des bénévoles'
        message_body = 'Merci de vous connecter à la plateforme.'

    # print(subject)
    # print(message_body)

    emails_pre = []
    for i in to_user:
        if i != from_user:
            # print(i)
            email = (subject, message_body, email_gmail, [i.email])
            emails_pre.append(email)
    emails = tuple(emails_pre)

    try:
        send_mass_mail(emails)
    except smtplib.SMTPAuthenticationError as e:
        print(f"auth error: {e}")
    except:
        print('other error')

    # send_mail(
    # subject,
    # message_body,
    # email_gmail,
    # [to_user.email],
    # fail_silently=False,)


# emails = (
#     ('Hey Man', "I'm The Dude! So that's what you call me.", 'dude@aol.com', ['mr@lebowski.com']),
#     ('Dammit Walter', "Let's go bowlin'.", 'dude@aol.com', ['wsobchak@vfw.org']),
# )
# results = mail.send_mass_mail(emails)
