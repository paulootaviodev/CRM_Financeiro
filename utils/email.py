from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse

def generate_email_verification_link(request, user: object) -> str:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    link = f"{request.scheme}://{request.get_host()}{url}"
    return link

def send_verification_email(request, user: object) -> None:
    link = generate_email_verification_link(request, user)
    subject = "Valide seu e-mail"
    message = f"Por favor, clique no link a seguir para validar seu e-mail: {link}"
    send_mail(subject, message, 'seu-email@exemplo.com', [user.email])
