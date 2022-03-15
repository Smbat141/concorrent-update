FROM python:3.8
RUN apt-get update && apt-get install -y python3-pip
RUN pip install pipenv
COPY . /projects
WORKDIR /projects
RUN pipenv install --system --deploy --ignore-pipfile
ENV PYTHONPATH "${PYTHONPATH}:."
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]