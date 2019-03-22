FROM python:3.7

ENV PYTHONUNBUFFERED 1 \
  PYTHONHASHSEED=random \
  TZ=Europe/Moscow

# Install requirements
COPY pyproject.toml poetry.lock /
RUN pip install poetry \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev -n -q --no-ansi

COPY ./etc/run-worker.sh /run-worker.sh
RUN chmod +x /run-worker.sh

WORKDIR /app

# Run server
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
