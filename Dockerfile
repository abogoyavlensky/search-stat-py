FROM python:3.7

ENV PYTHONUNBUFFERED 1 \
  PYTHONHASHSEED=random \
  TZ=Europe/Moscow

# Install requirements
COPY pyproject.toml poetry.lock /
RUN pip install poetry \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev

WORKDIR /app

# Run server
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
