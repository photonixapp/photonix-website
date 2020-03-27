build:
	docker-compose build

start:
	docker-compose up

stop:
	docker-compose kill

restart:
	docker-compose restart website

clean:
	docker-compose rm

shell:
	docker-compose exec website bash
