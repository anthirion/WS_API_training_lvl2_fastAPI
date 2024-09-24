FROM python:3.12
# Dossier du conteneur
WORKDIR /app
# Le premier . désigne le dossier où se trouve le Dockerfile
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]