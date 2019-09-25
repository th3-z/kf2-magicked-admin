FROM python:3

COPY magicked_admin /magicked_admin

RUN pip install -r requirements.txt

WORKDIR /magicked_admin

CMD [ "python", "magicked_admin.py", "-s"]