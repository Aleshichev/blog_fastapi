run:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

build:
	docker-compose up --build

start:
	uvicorn src.main:app --reload

	
