FROM python:3.7

ENV PYTHONUNBUFFERED 1 \
  PYTHONHASHSEED=random \
  TZ=Europe/Moscow

# Install requirements
COPY . /app
WORKDIR /app
RUN pip install poetry \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev

CMD ["python", "main.py"]
