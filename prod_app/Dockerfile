FROM python:3.12
# Changement de dossier dans le filesystem du conteneur
WORKDIR /app
# Le premier . désigne le chemin du PC et le deuxième le chemin du conteneur
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]