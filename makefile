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

lint:
	@# TODO: Slowly remove ignores
	@flake8 --ignore F405,E501,F403,E722,W503,F401

.PHONY: build

