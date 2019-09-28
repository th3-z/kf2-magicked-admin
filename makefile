NO_COLOR=\033[0m
GREEN_COLOR=\033[32m
RED_COLOR=\033[31m
YELLOW_COLOR=\033[33;01m

build:
	@python3 magicked_admin/setup.py build -b bin

clean:
	-@rm -rf bin
	-@rm -rf magicked_admin/*.sqlite
	-@rm -rf magicked_admin/magicked_admin.conf
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +

run:
	-@./bin/magicked_admin

isort:
	@sh -c "isort --recursive ."

pytest:
	@echo "\n$(YELLOW_COLOR)Running tests...$(NO_COLOR)\n"
	@pytest tests --cov-fail-under=1 --cov=magicked_admin


lint:
	@echo "$(YELLOW_COLOR)Checking lints...$(NO_COLOR)\n"
	@flake8 --ignore F405,F403,W503,F401 --exclude=admin_patches/utils/patch.py && \
		echo "$(GREEN_COLOR)success!$(NO_COLOR)" \
		|| { echo "$(RED_COLOR)failure!$(NO_COLOR)\n"; exit 1; }

test: lint pytest


.PHONY: build

