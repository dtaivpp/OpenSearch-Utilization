FROM python:3
LABEL MAINTAINER="David Tippett"

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /code
COPY . .

CMD python /code/github-collector/runner.py
