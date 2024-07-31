FROM python:3.12-slim
RUN pip install poetry
RUN apt-get update  && apt-get install -y gcc
COPY .. /app/
WORKDIR /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev
EXPOSE 5000

CMD  ["poetry", "run", "python3", "-m", "notimy"]
