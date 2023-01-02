FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tolo

RUN pip install --upgrade pip
COPY requirementes.txt /tolo/requirementes.txt
RUN pip install -r requirementes.txt

COPY . /tolo/