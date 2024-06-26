FROM python:3.9

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY . /code

RUN pip install cmake && pip install -r requirements.txt

EXPOSE 8101

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8101  
