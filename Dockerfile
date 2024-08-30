FROM python:3.12
COPY with_db_container/ app/
COPY requirements.txt app/
COPY start_api_server.sh app/
RUN pip install -r app/requirements.txt
EXPOSE 80
# Get wait-for-it script to wait until db server is up to the launch api server
RUN git clone https://github.com/vishnubob/wait-for-it.git
RUN chmod +x wait-for-it/wait-for-it.sh