FROM python:3.10
COPY with_db/ app/
COPY requirements.txt app/
RUN pip install -r app/requirements.txt
EXPOSE 80
# check that .env file is copied
# CMD ["ls", "-a", "/app"]
CMD ["fastapi", "dev", "app/main.py"]