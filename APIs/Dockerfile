FROM python:3.13-slim

WORKDIR /api

RUN pip install flask  mysql-connector-python  Flask-HTTPAuth  Flask-Cors

COPY RecipeByName.py .
COPY setting.ini .

EXPOSE 5000

ENTRYPOINT [ "python","RecipeByName.py" ]