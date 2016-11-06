# stop all running dockers
all-stop:
	-docker stop grenouillebot
	-docker rm grenouillebot

# start all
all-start:
	docker-compose -p grenouillebot -f docker/docker-compose.yml up -d --build

# run bot
bot-run:
	docker-compose -p grenouillebot -f docker/docker-compose.yml up --build grenouillebot

# build
build:
	docker-compose -p grenouillebot -f docker/docker-compose.yml build
