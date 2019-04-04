magicked_admin:
	@python3 magicked_admin/setup.py build -b bin

clean:
	-@rm -rf bin
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +

isort:
	@sh -c "isort --recursive ."

lint:
	@flake8

.PHONY: magicked_admin

