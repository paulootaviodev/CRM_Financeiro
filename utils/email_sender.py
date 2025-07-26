from os import getenv

from django.core.mail import send_mail
from django.core import signing
from django.urls import reverse

def generate_custom_token(client):
    value = f"{client.pk}:{client.slug}:{client.cpf_hash}"
    return signing.dumps(value)

def check_custom_token(token):
    try:
        value = signing.loads(token, max_age=86400)  # 24h
        pk, slug, cpf_hash = value.split(":")
        return pk, slug, cpf_hash
    except signing.BadSignature:
        return None

def generate_response_link(request, client, loan_proposal_slug, action):
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
    accept_link = generate_response_link(request, loan_proposal.client, loan_proposal.slug, 'accept')
    refuse_link = generate_response_link(request, loan_proposal.client, loan_proposal.slug, 'refuse')

    html_message = f"""
        <p>Você recebeu uma proposta de empréstimo.</p>
        <a href="{accept_link}" class="btn btn-success">Aceitar</a>
        <a href="{refuse_link}" class="btn btn-danger">Recusar</a>
    """

    send_mail(
        'Proposta de Empréstimo',
        'Escolha uma opção para continuar.',
        getenv('SMTP_EMAIL'),
        [loan_proposal.client.email],
        html_message=html_message
    )
