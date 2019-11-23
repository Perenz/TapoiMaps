FROM python:3

ADD . /

RUN pip install numpy
RUN pip install Cython
COPY requirements.txt /
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 8080

CMD ["python", "./src/app.py"]