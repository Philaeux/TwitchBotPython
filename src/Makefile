# Windows environment
## Create a virtual environment and install dependencies
win-install:
	python -m venv .wvenv
	.\.wvenv\Scripts\python.exe -m pip install --upgrade pip
	.\.wvenv\Scripts\python.exe -m pip install -r .\requirements.txt
	"$(get-location)" > .\.wvenv\Lib\site-packages\bot.pth

## Run the development files
win-run:
	.\.wvenv\Scripts\python.exe .\app.py

## Remove development environment
win-clean:
	rm -r .wvenv

## Generate a production build
win-build:
	.\.wvenv\Scripts\pyinstaller.exe --distpath ../build/dist --workpath ../build --onedir -n twitchbot --add-data ".\default\settings.ini;." --add-data ".\default\sqlite.db;." --add-data ".\bot\data;data" .\app.py

## Move the development database to latest migration
win-db-upgrade:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe upgrade head

## Move the development database back by one migration
win-db-downgrade:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe downgrade -1

## Generate a new database migration by scanning Models files
win-db-migrate:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe revision --autogenerate

# Unix environment
## Create a virtual environment and install dependencies
unix-install:
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r requirements.txt
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/bot.pth &&) echo

## Run the development files
unix-run:
	.venv/bin/python3 app.py

## Remove development environment
unix-clean:
	rm -rf .venv

## Move the development database to latest migration
unix-db-upgrade:
	export PYTHONPATH=${PWD} | .venv/bin/alembic upgrade head

## Move the development database back by one migration
unix-db-downgrade:
	export PYTHONPATH=${PWD} | .venv/bin/alembic downgrade -1

## Generate a new database migration by scanning Models files
unix-db-migrate:
	export PYTHONPATH=${PWD} | .venv/bin/alembic revision --autogenerate
