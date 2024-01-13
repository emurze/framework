
make run_server:
	poetry run python src/run.py

types:
	poetry run mypy tests src

unittests:
	poetry run pytest -s tests

test: types unittests
