FROM python:3.9
ENV PYTHONUNBUFFERED 1
#COPY . /usr/src/app
#WORKDIR 
WORKDIR /app


COPY requirements.txt requirements.txt

RUN python -m pip install -U pip

RUN pip install --upgrade pip

RUN pip install mysql-connector-python


RUN pip --version

RUN pip install -r requirements.txt 



COPY . .


CMD [ "python","manage.py","runserver","0.0.0.0:8000"]#
