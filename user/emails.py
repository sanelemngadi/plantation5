from django.core.mail import send_mail, EmailMultiAlternatives
from user.models import PlantationUser
from backend.settings import EMAIL_HOST_USER

def email_user(user: PlantationUser, subject: str, msg: str):
    recipient_list = [user.email]  # Replace with the recipient's email address
    send_mail(subject, msg, EMAIL_HOST_USER, recipient_list, fail_silently=False)


def email_any(subject: str, msg: str, email: str):
    recipient_list = [email]  # Replace with the recipient's email address
    send_mail(subject, msg, EMAIL_HOST_USER, recipient_list, fail_silently=False)

def attach_image_email(user: PlantationUser, subject: str, message: str, img_path: str):
    from_email = EMAIL_HOST_USER
    recipient_list = [user.email]
    reply_to = [EMAIL_HOST_USER]

    email = EmailMultiAlternatives(subject, message, from_email, recipient_list, reply_to=reply_to)
    email.attach_file(img_path, mimetype='image/png')

    # Send the email
    email.send()


