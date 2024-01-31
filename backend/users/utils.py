from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, user, token_id):
    data = {
        'user': user,
        'token_id': token_id
    }

    html_message = get_template('users/email_message_confirm.html').render(data)

    send_mail(
        subject='Confirm your email',
        message=None,
        html_message=html_message,
        from_email='admin@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )
