# Dev tests without docker

dev-install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install -r requirements.txt
	make dev-path-install

dev-path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/grenouillebot.pth &&) echo

dev-run:
	.venv/bin/python3 bot/bot_application.py

dev-clean:
	rm -rf .venv

# Prod docker

build:
	docker-compose -f docker/docker-compose.yml build

prod-start:
	docker-compose -f docker/docker-compose.yml up -d --build

prod-stop:
	docker-compose -f docker/docker-compose.yml down
