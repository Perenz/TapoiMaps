FROM python:3
ADD src/app.py /

RUN pip install -r requirements.txt

CMD ["python", "./src/app.py"]