FROM python:3.12 as python-base

RUN mkdir app

WORKDIR  /app

COPY /pyproject.toml /app

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install 

COPY . .

CMD ["poetry", "run", "start"]
