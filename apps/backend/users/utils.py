from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from users.tokens import account_activation_token

def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_path = reverse("users:activate", kwargs={"uidb64": uid, "token": token})
    activation_link = request.build_absolute_uri(activation_path)

    subject = "Activate your account"
    message = render_to_string("users/activation_email.html", {
        "user": user,
        "activation_link": activation_link,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()
