run:
	python -m src

test: export RUN_INTEGRATION_TESTS = 0
test:
	coverage run --source=./src -m pytest tests/

report:
	coverage report -m

auto_test:
	python -m pytest_watch -c --runner "python -m pytest"

build_dependencie_dev:
	pip-compile --allow-unsafe dev-requirements.in

build_dependencie_prod:
	pip-compile --allow-unsafe requirements.in
