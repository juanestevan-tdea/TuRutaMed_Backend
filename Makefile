up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f backend

shell:
	docker compose exec backend bash

reset:
	docker compose down -v
