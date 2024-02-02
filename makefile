build:
	docker-compose build

up:
	docker-compose up -d

dev:
	docker-compose up -d --build

exec:
	docker-compose exec app bash

down:
	docker-compose down