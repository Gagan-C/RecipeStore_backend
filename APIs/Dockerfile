FROM python

RUN apt update
WORKDIR /api


RUN pip install flask  mysql-connector-python  Flask-HTTPAuth  Flask-Cors

COPY RecipeByName.py .
COPY setting.ini .

EXPOSE 5000

ENTRYPOINT [ "python","RecipeByName.py" ]