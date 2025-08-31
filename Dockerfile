FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./log_conf.yaml /code/log_conf.yaml


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--log-config=log_conf.yaml"]