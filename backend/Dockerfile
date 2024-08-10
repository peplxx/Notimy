FROM python:3.12-slim

# RUN apt-get update  && apt-get install -y gcc

RUN pip install poetry


WORKDIR /app/

COPY ./poetry.lock .
COPY ./pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN poetry add pyopenssl

COPY . .

EXPOSE 5000

CMD  ["poetry", "run", "python3", "-m", "notimy"]
