FROM python:3.10
COPY with_db/ app/
COPY requirements.txt app/
RUN pip install -r app/requirements.txt
EXPOSE 80
CMD ["ls", "/app"]
#  CMD ["fastapi", "dev", "app/main.py"]