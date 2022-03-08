build-image:
	docker build -t spark ./infra

start-infra:
	docker-compose up
