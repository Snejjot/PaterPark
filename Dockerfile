# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ADD . /code
WORKDIR /code
COPY . /code
RUN ls -la
RUN pip3 install -r requirements.txt
RUN pytest test_app.py -vvv
RUN rm testpeterpark.sqlite3

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]