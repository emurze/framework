
coverage:
	bash -c "cd src && coverage run server/run.py && coverage report"

run:
	poetry run python src/server/run.py app:app

types:
	poetry run mypy tests src

unittests:
	poetry run pytest -s tests

test: types unittests
