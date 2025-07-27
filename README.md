# GrenouilleBot
Twitch chat (IRC) bot giving additional streaming features.

## Run

```
cd src
uv run python main.py
```

## Configuration
The bot loads the configuration from `settings.ini`.  
Create your own following the structure of the example file at `settings.example.ini`.  
To run the bot, you need a Twitch Account (login, password, oauthToken).  

The database is stored in a `sqlite.db` file if you didn't specify any database url.  
The file is in `src/bot/models` in development, or next to binaries in prod.

## Project structure
The `src` folder contains all the development code, but also scripts to run the application or update the database.   
The `src/bot` folder contains the application code, divided as follows:
- `bot` - The master application creating modules used in the whole application.
- `models` - Database models and database client.
- `irc_client` - The IRC bot listening to the Twitch chat commands/rewards calling handlers.
- `gui` - QT Application used to display one window and play sound (TODO: replace with web server).
- `strategy` - Event handlers management using processors.
- `processors/bet_processor` - Processor managing user bets.
- `processors/sound_processor` - Processor managing user sound requests.
