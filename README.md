# GrenouilleBot
Twitch chat (IRC) bot giving additional streaming features.

## Development commands
`(system)` is either `win` or `unix`.
- `make (system)-install` - create the python virtual environment.
- `make (system)-run` - start the bot.

- `make (system)-db-upgrade` - update the database (run all migrations).
- `make (system)-db-downgrade` - downgrade the database (one version).
- `make (system)-db-migrate` - generate migration from models.

## Production setup on UNIX server
Setup a `systemd` service by creating a file similar to `prod/twitchbot.service` into `/etc/systemd/system/`.  
CHMOD it to 644. Remember to edit the application settings.  

## Production setup on WINDOWS server
Use the binaries from GitHub to start the bot. Remember to edit the application settings.  

## Configuration
The bot loads the configuration from `settings.ini`.  
Create your own following the structure of the example file at `settings.example.ini`.  
To run the bot, you need a Twitch Account (login, password, oauthToken).

## Project structure
The `bot` folder contains the application code, divided as follows:
- `bot` - The master application creating modules used in the whole application.
- `models` - Database models.
- `module/irc` - The IRC bot listening to the Twitch chat commands with methods to answer.
- `module/calendar` - Calendar module loading events from the Google Calendar to display in chat.
- `module/commands` - Logic of all the commands managed by the bot, strategy pattern.
- `module/wiki` - Old module used to parse dota 2 wiki.

