FROM python:3.12-alpine
WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install -U pip setuptools && pip install -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh && find . -name "*.pyc" -delete

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
