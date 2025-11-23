from django.conf import settings
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_activation_email(user, request):
    """Створює та відправляє листа для активації акаунта."""
    activation_link = f"{request.scheme}://{request.get_host()}/users/activate/{user.email_confirmation_token}/"

    # Plain text + HTML
    message_txt = render_to_string("users/email_confirmation_message.txt", {
        "user": user,
        "activation_link": activation_link,
    })

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Activate your account",
        plain_text_content=message_txt,
    )

    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        sg.send(message)
    except Exception as e:
        print(f"SendGrid error: {e}")