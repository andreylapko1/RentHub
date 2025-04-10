FROM python:3.12


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --verbose


COPY . .

ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT:-3306}


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# andreylapko1/renthub