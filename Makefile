format:
		black -S --line-length 120 ./src

test:
		python -m unittest discover .

sort-imports:
		isort ./src

ci:
		sort-imports format test 
