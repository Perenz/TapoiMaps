FROM python:3
ADD web/app.py /

RUN pip install requirements.txt

CMD ["python", "./web/app.py"]\