# Ponto de entrada para hospedagem: gunicorn wsgi:app
from app import create_app

app = create_app()
