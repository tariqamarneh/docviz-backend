FROM python:3.12.2

RUN pip install poetry==1.7.1

COPY . .

RUN poetry install

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "start"]
