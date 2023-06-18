FROM python:3.11

WORKDIR /Django_Restaurant

COPY .env /Django_Restaurant/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY db.sqlite3 /Django_Restaurant/

RUN python manage.py collectstatic --no-input

EXPOSE 8888

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]

