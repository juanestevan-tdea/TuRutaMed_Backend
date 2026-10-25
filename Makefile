.PHONY: up up-dev down logs ps shell reset test-backend test-frontend

up:
	docker compose up --build -d

up-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

down:
	docker compose down

logs:
	docker compose logs -f backend frontend

ps:
	docker compose ps

shell:
	docker compose exec backend bash

reset:
	docker compose down -v

test-backend:
	pytest -q

test-frontend:
	cd TuRutaMed_Frontend && npm ci && npm run lint && npm run build
