import os

MONGO = str(os.environ.get("MONGO"))
MONGO_DATABASE = str(os.environ.get("MONGO_DATABASE"))
RABBITMQ_URI = str(os.environ.get("RABBITMQ_URI"))

QUEUE_NAME = str(os.environ.get("QUEUE_NAME"))

SENDGRID_API_KEY = str(os.environ.get("SENDGRID_API_KEY"))
SMTP_REMETENTE = str(os.environ.get("SMTP_REMETENTE"))
