FROM python:3.10-slim
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY . /app/
RUN poetry install --no-root
CMD ["sh", "start.sh"]