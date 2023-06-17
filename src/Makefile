# Dev tests without docker

win-install:
	python -m venv .wvenv
	.\.wvenv\Scripts\python.exe -m pip install --upgrade pip
	.\.wvenv\Scripts\python.exe -m pip install -r .\requirements.txt
	"$(get-location)" > .\.wvenv\Lib\site-packages\bot.pth

unix-install:
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r requirements.txt
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/grenouillebot.pth &&) echo

win-run:
	.\.wvenv\Scripts\python.exe .\app.py

unix-run:
	.venv/bin/python3 app.py

win-build:
	.\.wvenv\Scripts\pyinstaller.exe --distpath ../build/dist --workpath ../build --onedir -n twitchbot --add-data ".\default\settings.ini;." --add-data ".\default\sqlite.db;." --add-data ".\bot\data;data" .\app.py

win-clean:
	rm -r .wvenv

unix-clean:
	rm -rf .venv

# DATABASE
win-db-upgrade:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe upgrade head

unix-db-upgrade:
	export PYTHONPATH=${PWD} | .venv/bin/alembic upgrade head

win-db-downgrade:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe downgrade -1

unix-db-downgrade:
	export PYTHONPATH=${PWD} | .venv/bin/alembic downgrade -1

win-db-migrate:
	$env:PYTHONPATH="$(get-location)" ; .\.wvenv\Scripts\alembic.exe revision --autogenerate

unix-db-migrate:
	export PYTHONPATH=${PWD} | .venv/bin/alembic revision --autogenerate
