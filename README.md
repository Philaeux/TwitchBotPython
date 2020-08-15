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

## Production setup on WINDOWS
Use the binaries from GitHub to start the bot. Remember to edit the application settings.  

## Configuration
The bot loads the configuration from `settings.ini`.  
Create your own following the structure of the example file at `settings.example.ini`.  
To run the bot, you need a Twitch Account (login, password, oauthToken).  

The database is stored in a `sqlite.db` file if you didn't specify any database url.  
The file is in `src/bot/models` in developement, or next to binaries in prod.  
The database is updated if necessary at start time. (TODO)

## Project structure
The `src` folder contains all the development code, but also scripts to run the application or update the database.   
The `src/bot` folder contains the application code, divided as follows:
- `bot` - The master application creating modules used in the whole application.
- `models` - Database models and database client.
- `irc_client` - The IRC bot listening to the Twitch chat commands/rewards calling handlers.
- `gui` - Application QT used to display one window and play sound (TODO: replace with web server).
- `strategy` - Event handlers management using processors.
- `processors/bet_processor` - Processor managing user bets.
- `processors/sound_processor` - Processor managing user sound requests.
