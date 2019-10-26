FROM python:3

COPY magicked_admin /magicked_admin
COPY docker_startup.sh /magicked_admin/docker_startup.sh
COPY admin_patches /magicked_admin_patches
COPY requirements.txt /magicked_admin/requirements.txt

RUN pip install -r /magicked_admin/requirements.txt

WORKDIR /magicked_admin

CMD ["/magicked_admin/docker_startup.sh"]
