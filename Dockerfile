FROM python:3

COPY magicked_admin /magicked_admin
COPY requirements.txt /magicked_admin/requirements.txt

RUN pip install -r /magicked_admin/requirements.txt

WORKDIR /magicked_admin

CMD [ "python", "magicked_admin.py", "-s"]
