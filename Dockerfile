FROM python:3.12-slim
RUN pip install poetry
RUN apt-get update  && apt-get install -y gcc
COPY /notimy /app/notimy/
COPY poetry.lock /app/
COPY .env /app/
COPY alembic.ini /app/
COPY /migration /app/migration/
COPY pyproject.toml /app/
WORKDIR /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev
EXPOSE 5000

CMD  ["poetry", "run", "python3", "-m", "notimy"]
