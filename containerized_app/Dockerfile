FROM python:3.12
# Dossier du conteneur
WORKDIR /app
# Le premier . désigne le chemin du PC et le deuxième le chemin du conteneur
COPY . .
COPY ../requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]