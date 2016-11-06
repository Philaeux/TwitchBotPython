# GrenouilleBot
Twitch chat (IRC) bot for the FroggedTV.

## Dependencies

- `Makefile`
- [Docker engine](https://www.docker.com/products/docker-engine) and [docker-compose](https://docs.docker.com/compose/)

## Commands

- `make build` - build the docker image used
- `make bot-run` - start the bot attached to see logs (dev)
- `make all-start` - start the bot detached (prod)
- `make all-stop` - stop the bot if detached (prod)

## About configurations

The bot configuration is saved and loaded from `bot/settings.ini`. The file is encoded using [transcrypt](https://github.com/elasticdog/transcrypt) and a secret key. However, you can have a peek at the structure with the `bot/settings.example.ini` file.

To run the bot, you need a Twitch Account (login, password, oauthToken) and a GoogleAPIKey with GoogleCalendar access.

## Project structure

The bot is divided into 3 modules:
- `bot_application` - The master module creating the other two and orchestrating shared objects.
- `grenouille_calendar` - A periodic task to retrieve events from a google calendar.
- `grenouille_irc_bot` - The IRC bot listening to the Twitch chat and answering to commands.
