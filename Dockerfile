FROM python:latest
RUN apt-get update
WORKDIR /pythontest
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /pythontest
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]