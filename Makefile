# stop all running dockers
all-stop:
	-docker stop froggedtv_grenouillebot
	-docker rm froggedtv_grenouillebot

# start all
all-start:
	docker-compose -f docker/docker-compose.yml up -d --build

# start bot
bot-start:
	docker-compose -f docker/docker-compose.yml up --build froggedtv_grenouillebot

# build
build:
	docker-compose -f docker/docker-compose.yml build
