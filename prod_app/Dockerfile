FROM laudio/pyodbc:3.0.0
# Changement de dossier dans le filesystem du conteneur
WORKDIR /app
# Définition des variables d'environnement
ENV USER="user"
ENV PSWD="WavestoneApiTraining01"
ENV PROTOCOL="tcp"
ENV HOST="mssql-main-server.database.windows.net"
ENV PORT="1433"
ENV DB_NAME="ws-api-training-shop-db"
# Le premier . désigne le chemin du PC et le deuxième le chemin du conteneur
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "run", "main.py"]