# GrenouilleBot
Twitch chat (IRC) bot for the FroggedTV.

## Dependencies

- `Makefile`
- [Docker engine](https://www.docker.com/products/docker-engine) and [docker-compose](https://docs.docker.com/compose/)

## Commands

- `make build` - build the docker image used in prod.
- `make prod-start` - start the bot detached (prod).
- `make prod-stop` - stop the bot if detached (prod).

## About configurations


The bot configuration is saved and loaded from `bot/settings.ini`. 
Create your own following the structure of the example file at `bot/settings.example.ini`.
To run the bot, you need a Twitch Account (login, password, oauthToken) and a GoogleAPIKey with GoogleCalendar access.

The docker production module needs a `docker/docker-compose.yml` setup according to your system choices.
You have a file example with `docker/docker-compose.example.yml`.


## Project structure

Docker image and configuration are stored in the `docker` folder.  

The `bot` folder contains the application code, divided as follow:
- `bot_application` - The master application creating modules used in the whole application.
- `module/irc` - The IRC bot listening to the Twitch chat commands with methods to answer.
- `module/calendar` - Calendar module keeping a picture of the Google Calendar of the web TV.
- `module/commands` - Logic of all the commands managed by the bot.
