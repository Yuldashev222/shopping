FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/shopping

COPY ./reqs.txt /usr/src/reqs.txt
RUN pip install -r /usr/src/reqs.txt

COPY . /usr/src/shopping

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
