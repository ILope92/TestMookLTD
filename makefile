all:
	@echo "make db			- Start postgres container"
	@echo "make app			- Start app container"
	@echo "make devenv      - install enviroment python3.11"
	@echo "make compose     - build and run app, db services"
	@exit 0

clean:
	rm -rf venv

devenv: clean
	# создаем новое окружение
	apt-get install python3-venv
	python3.11 -m venv env
	env/bin/python3.11 -m pip install pip --upgrade
	env/bin/python3.11 -m pip install wheel
	# ставим зависимости
	env/bin/python3.11 -m pip install -r requirements.txt

redis:
	docker stop mookltd-redis-test || true
	docker compose run -d -p 6379:6379 --name mookltd-redis-test

database:
	docker stop mookltd-db-test || true
	docker compose run -d -p 6379:6379 --name mookltd-db-test

celery:
	docker stop mookltd-celery-test || true
	docker compose run -d -p 6379:6379 --name mookltd-celery-test

nginx:
	docker stop mookltd-nginx-test || true
	docker compose run -d -p 6379:6379 --name mookltd-nginx-test

app:
	docker stop mookltd-app-test || true
	docker compose run -d -p 8002:8002 --name mookltd-app-test

compose:
	docker compose up --build -d