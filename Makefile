format:
		docker exec pythonapp black -S --line-length 120 ./src

test:
		docker exec pythonapp python3 -m unittest discover .

sort-imports:
		docker exec pythonapp isort ./src

ci: sort-imports format test 

up:
		docker compose up

down:
		docker compose down

run:
		docker exec pythonapp python3 ./src/pipeline/run.py

display:
		docker exec pythonapp python3 ./src/pipeline/dashboard.py
