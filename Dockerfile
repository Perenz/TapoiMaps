FROM python:3

ADD . /

RUN pip install numpy
RUN pip install Cython
COPY requirements.txt /
RUN pip install -r requirements.txt

CMD ["python", "./src/app.py"]