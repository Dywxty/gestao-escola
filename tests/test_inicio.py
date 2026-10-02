from app import app


cliente = app.test_client()

def test_inicio_status_code():
    resposta = cliente.get("/")

    assert resposta.status_code == 200


def test_inicio_message():
    resposta = cliente.get("/")

    assert resposta.get_data(as_text=True) == "Sistema de Gerenciamento Escolar"