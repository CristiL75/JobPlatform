# Dockerfile for Django

# Folosește o imagine oficială Python ca bază
FROM python:3.9-slim

# Setează variabilele de mediu pentru a evita crearea de fișiere pyc și pentru a forța terminalul să fie non-interactiv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierul requirements.txt în directorul de lucru
COPY requirements.txt /app/

# Instalează dependențele din requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiază conținutul aplicației Django în directorul de lucru
COPY . /app/

# Expune portul pe care rulează Django (implicit 8000)
EXPOSE 8000

# Rulează comanda de pornire a serverului Django
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
