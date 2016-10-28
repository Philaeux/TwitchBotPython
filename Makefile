# stop all running dockers
all-stop:
	-docker stop grenouillebot
	-docker rm grenouillebot

# start all
all-start:
	docker-compose -f docker/docker-compose.yml up -d --build

# start bot
bot-start:
	docker-compose -f docker/docker-compose.yml up --build grenouillebot

# build
build:
	docker-compose -f docker/docker-compose.yml build
