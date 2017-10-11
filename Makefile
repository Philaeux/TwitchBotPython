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
	docker-compose -p grenouillebot -f docker/docker-compose.yml build

prod-stop:
	-docker stop grenouillebot
	-docker rm grenouillebot

prod-start:
	docker-compose -p grenouillebot -f docker/docker-compose.yml up -d --build
