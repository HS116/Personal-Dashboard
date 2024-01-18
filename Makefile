format:
		black -S --line-length 120 ./src

test:
		python -m unittest discover .

sort-imports:
		isort ./src

ci: sort-imports format test 

up:
		docker compose up

run:
		docker exec pythonapp python3 ./src/pipeline/run.py

display:
		docker exec pythonapp python3 ./src/pipeline/dashboard.py