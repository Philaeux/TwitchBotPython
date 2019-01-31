# GrenouilleBot
Twitch chat (IRC) bot.

## Dev commands

- `make install` - create the python virtual environment.
- `make run` - start the bot.

- `make db-upgrade` - update the database (run all migrations).
- `make db-downgrade` - downgrade the database (one version).
- `make db-migrate` - generate migration from models.

## Prod

Setup a `systemd` service by creating a file similar to `prod/twitchbot.service` into `/etc/systemd/system/`. 

CHMOD it to 644.

## Configuration

The bot configuration is saved and loaded from `bot/settings.ini`. 
Create your own following the structure of the example file at `bot/settings.example.ini`.
To run the bot, you need a Twitch Account (login, password, oauthToken).

## Project structure

The `bot` folder contains the application code, divided as follow:
- `bot_application` - The master application creating modules used in the whole application.
- `models` - Database models.
- `module/irc` - The IRC bot listening to the Twitch chat commands with methods to answer.
- `module/calendar` - Calendar module keeping a picture of the Google Calendar of the web TV.
- `module/commands` - Logic of all the commands managed by the bot.
