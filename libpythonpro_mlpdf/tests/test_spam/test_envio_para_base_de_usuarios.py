import pytest

from libpythonpro_mlpdf.spam.enviador_de_email import Enviador
from libpythonpro_mlpdf.spam.main import EnviadorDeSpam
from libpythonpro_mlpdf.spam.modelos import Usuario


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Matheus', email='matheuslopes.pdf@gmail.com'),
            Usuario(nome='Gabriel', email='matheuslopes.pdf@gmail.com')
        ],
        [
            Usuario(nome='Gabriel', email='matheuslopes.pdf@gmail.com')
        ]
    ]
)
def test_qte_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    enviador = EnviadorMock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'matheuslopes.pdf@gmail.com',
        'Curso Python Pro',
        'Corpo'
    )
    assert len(usuarios) == enviador.qtd_email_enviados


class EnviadorMock(Enviador):
    def __init__(self):
        super().__init__()
        self.qtd_email_enviados = 0
        self.parametros_de_envio = None

    def enviar(self, remetente, destinatario, assunto, corpo):
        self.parametros_de_envio = (remetente, destinatario, assunto, corpo)
        self.qtd_email_enviados += 1


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Matheus', email='matheuslopes.pdf@gmail.com')
    sessao.salvar(usuario)
    enviador = EnviadorMock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'teste@gmail.com',
        'Curso Python Pro',
        'Corpo'
    )
    assert enviador.parametros_de_envio == (
        'teste@gmail.com',
        'matheuslopes.pdf@gmail.com',
        'Curso Python Pro',
        'Corpo'
    )