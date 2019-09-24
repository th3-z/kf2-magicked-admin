FROM python:3

COPY magicked_admin /magicked_admin

RUN pip install colorama termcolor lxml requests

WORKDIR /magicked_admin

CMD [ "python", "magicked_admin.py", "-s"]