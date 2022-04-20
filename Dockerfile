FROM python:3.10

WORKDIR /usr/src/requests_app

COPY . .

RUN pip install -r requirements.txt

EXPOSE ${APP_PORT}

#CMD bash wait-for-it.sh -t 0 mysql_container:6603 -- pipenv run python server.py

CMD ["python", "server.py"]
