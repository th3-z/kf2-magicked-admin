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
	@flake8 --ignore F405,E501

.PHONY: build

