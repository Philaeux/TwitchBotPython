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
The production file is not inside the repository. 
Create your own following the structure of the example file at `bot/settings.example.ini`.

To run the bot, you need a Twitch Account (login, password, oauthToken) and a GoogleAPIKey with GoogleCalendar access.
`grenouille_api_key` is a secret you must define to secure access to the web server from outside. 

## Project structure

Docker image and configuration are stored in the `docker` folder.  

The `bot` folder contains the application code, divided as follow:
- `bot_application` - The master application creating modules used in the whole application.
- `module/webserver` - Web server accepting POST requests from the outside to execute commands.
- `module/irc` - The IRC bot listening to the Twitch chat commands with methods to answer.
- `module/calendar` - Calendar module keeping a picture of the Google Calendar of the web TV.
- `module/commands` - Logic of all the commands managed by the bot.
