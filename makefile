NO_COLOR=\033[0m
GREEN_COLOR=\033[32m
RED_COLOR=\033[31m
YELLOW_COLOR=\033[33;01m

PYTHON3_OK = $(shell python3 --version 2> /dev/null | wc -l)
ifneq ('$(PYTHON3_OK)', '')
	PYTHON = "python3"
endif
PYTHON_OK = $(shell python --version 2> /dev/null | wc -l)
ifneq ('$(PYTHON_OK)', '')
	PYTHON = "python"
endif

ifndef PYTHON
	$(error "Couldn't find Python")
endif

all: clean build

build:
	@$(PYTHON) magicked_admin/setup.py build -b bin/magicked_admin
	@$(PYTHON) admin_patches/setup.py build -b bin/admin_patches

i18n-init:
	@pybabel extract admin_patches -o locale/admin_patches.pot
	@pybabel init -l en_GB -i locale/admin_patches.pot -d locale -o ./locale/en_GB/admin_patches.po
	@pybabel extract magicked_admin -o locale/magicked_admin.pot
	@pybabel init -l en_GB -i locale/magicked_admin.pot -d locale -o ./locale/en_GB/magicked_admin.po

clean:
	-@rm -rf bin
	-@rm -rf magicked_admin/conf/*.sqlite
	-@rm -rf magicked_admin/conf/magicked_admin.conf
	-@rm -rf magicked_admin/conf/magicked_admin.log
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +

run:
	-@./bin/magicked_admin/magicked_admin

isort:
	@sh -c "isort --recursive ."

pytest:
	@echo "\n$(YELLOW_COLOR)Running tests...$(NO_COLOR)\n"
	@pytest magicked_admin/tests --cov=magicked_admin


lint:
	@echo "$(YELLOW_COLOR)Checking lints...$(NO_COLOR)\n"
	@flake8 --ignore F405,F403,W503,F401,F811 --exclude=admin_patches/utils/patch.py && \
		echo "$(GREEN_COLOR)success!$(NO_COLOR)" \
		|| { echo "$(RED_COLOR)failure!$(NO_COLOR)\n"; exit 1; }

test: lint pytest


.PHONY: build clean

