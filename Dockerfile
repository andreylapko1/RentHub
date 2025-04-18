
FROM python:3.12

WORKDIR /RentHub


COPY . /RentHub/


RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py migrate


RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "RentHub.wsgi:application", "--bind", "0.0.0.0:8000"]
