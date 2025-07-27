from os import getenv

from django.core.mail import send_mail
from django.core import signing
from django.urls import reverse
from crm_financeiro.templatetags.custom_filters import format_currency

def generate_custom_token(client):
    """Create a token based on the client's pk, slug and cpf_hash."""

    value = f"{client.pk}:{client.slug}:{client.cpf_hash}"
    return signing.dumps(value)

def check_custom_token(token):
    """Check if client token is valid."""

    try:
        value = signing.loads(token, max_age=86400)  # 24h
        pk, slug, cpf_hash = value.split(":")

        return pk, slug, cpf_hash

    except signing.BadSignature as error:
        raise signing.BadSignature("Token inválido ou expirado.") from error


def generate_response_link(request, client, loan_proposal_slug, action):
    """Generate the email confirmation link using the token, slug and action (accept or refuse)."""

    token = generate_custom_token(client)
    url = reverse(
        'reply_loan_proposal',
        kwargs={
            'token': token,
            'slug': loan_proposal_slug,
            'action': action
        }
    )
    link = f"{request.scheme}://{request.get_host()}{url}"
    return link

def send_email_response(request, loan_proposal):
    """Send email to accept or decline loan proposal based on the proposal passed to the function."""

    accept_link = generate_response_link(request, loan_proposal.client, loan_proposal.slug, 'accept')
    refuse_link = generate_response_link(request, loan_proposal.client, loan_proposal.slug, 'refuse')

    released_value = format_currency(loan_proposal.released_value)
    value_of_installments = format_currency(loan_proposal.value_of_installments)
    number_of_installments = loan_proposal.number_of_installments

    html_message = f"""
        <p>Você recebeu uma proposta de empréstimo no valor de {released_value} em {number_of_installments}x de {value_of_installments}.</p>
        <a href="{accept_link}" style="padding:10px;background:#4CAF50;color:white;text-decoration:none;">Aceitar</a>
        <a href="{refuse_link}" style="padding:10px;background:#f44336;color:white;text-decoration:none;">Recusar</a>
    """

    send_mail(
        'Proposta de Empréstimo',
        'Escolha uma opção para continuar.',
        getenv('SMTP_EMAIL'),
        [loan_proposal.client.email],
        html_message=html_message
    )
