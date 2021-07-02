NO_COLOR=\033[0m
GREEN_COLOR=\033[32m
RED_COLOR=\033[31m
YELLOW_COLOR=\033[33;01m

PYTHON = "python3"

all: clean build

build:
	@$(PYTHON) magicked_admin/setup.py build -b bin/magicked_admin
	@$(PYTHON) admin_patches/setup.py build -b bin/admin_patches

i18n-update:
	@$(PYTHON) admin_patches/setup.py extract_messages --input-dirs "admin_patches" -o "admin_patches/locale/admin_patches.pot"
	@$(PYTHON) admin_patches/setup.py init_catalog -l en_GB -i "admin_patches/locale/admin_patches.pot" -d "admin_patches/locale" -o "./admin_patches/locale/en_GB/LC_MESSAGES/admin_patches.po"
	@$(PYTHON) magicked_admin/setup.py extract_messages --input-dirs "magicked_admin" -o magicked_admin/locale/magicked_admin.pot
	@$(PYTHON) magicked_admin/setup.py init_catalog -l en_GB -i "magicked_admin/locale/magicked_admin.pot" -d "magicked_admin/locale" -o "./magicked_admin/locale/en_GB/LC_MESSAGES/magicked_admin.po"

i18n-compile:
	@$(PYTHON) magicked_admin/setup.py compile_catalog -d "magicked_admin/locale" -D "magicked_admin"
	@$(PYTHON) admin_patches/setup.py compile_catalog -d "admin_patches/locale" -D "admin_patches"

clean:
	-@rm -rf bin
	-@rm -rf magicked_admin/conf/*.sqlite
	-@rm -rf magicked_admin/conf/magicked_admin.conf
	-@rm -rf magicked_admin/conf/magicked_admin.log
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +
	-@find . -name '*.mo' -exec rm -f {} +

isort:
	@sh -c "isort --recursive ."

lint:
	-@# F401 -- Unused import
	-@# F405 -- Name may be undefined
	-@# F403 -- Wildcard imports
	-@# W503 -- Line break before binary operator
	@echo "$(YELLOW_COLOR)Checking lints...$(NO_COLOR)\n"
	@flake8 --max-line-length 119 --ignore F401,F405,F403,W503 ./magicked_admin && \
		echo "$(GREEN_COLOR)success!$(NO_COLOR)" \
		|| { echo "$(RED_COLOR)failure!$(NO_COLOR)\n"; exit 1; }

test: lint pytest


.PHONY: build clean

