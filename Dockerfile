FROM python:3.12


WORKDIR /RentHub


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --verbose


COPY . /RentHub/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "rentapp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]



# andreylapko1/renthub