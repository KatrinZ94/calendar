from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'событие',
        'ваше событие начнется',
        'forallneedz@gmail.com',
        [user_email],
        fail_silently=False
    )
