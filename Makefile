.PHONY: install run test lint migrate docker-up docker-down

install:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio ruff

run:
	uvicorn app.main:app --reload

test:
	pytest -v

lint:
	ruff check app/ --select E,F,W --ignore E501

migrate:
	alembic upgrade head

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
