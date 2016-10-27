# stop all running dockers
all-stop:
	-docker stop froggedtv_junabot
	-docker rm froggedtv_junabot

# start all
all-start:
	docker-compose -f docker/docker-compose.yml up -d --build

# start bot
bot-start:
	docker-compose -f docker/docker-compose.yml up --build froggedtv_junabot

# build
build:
	docker-compose -f docker/docker-compose.yml build
