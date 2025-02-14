FROM python:3.13-slim

WORKDIR /api

RUN pip install flask  mysql-connector-python  Flask-HTTPAuth  Flask-Cors gunicorn

COPY RecipeByName.py .
COPY setting.ini .

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "RecipeByName:app" ]