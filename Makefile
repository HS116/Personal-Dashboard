format:
		black -S --line-length 120 ./src

test:
		python -m unittest discover .

sort-imports:
		isort ./src
