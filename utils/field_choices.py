STATE_CHOICES = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
    ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
    ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

EMPLOYMENT_STATUS  = [
    ('1', 'Funcionário Público'), ('2', 'Assalariado (CLT)'), ('3', 'Autônomo'), ('4', 'Empresário ou PJ'),
    ('5', 'Profissional Liberal'), ('6', 'Aposentado ou Pensionista'), ('7', 'Desempregado'),
    ('8', 'Programa Bolsa Família')
]

MARITAL_STATUS = [
    ('S', 'Solteiro(a)'), ('C', 'Casado(a)'), ('D', 'Divorciado(a)'), ('V', 'Viúvo(a)')
]

LOAN_PROPOSAL_STATUS = [
    ('0001', 'Gerada'), ('0002', 'Enviada para o cliente'), ('0003', 'Aceita'), ('0004', 'Recusada'),
    ('0005', 'Expirada'), ('0006', 'Cancelada'), ('0007', 'Em conferência'),
    ('0008', 'Paga na conta do cliente')
]

PAYMENT_STATUS = [
    ('0001', 'Em dia'), ('0002', 'Quitado'), ('0003', 'Atrasado'), ('0004', 'Inadimplente')
]
