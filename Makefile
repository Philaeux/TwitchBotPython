# Dev tests without docker

win-install:
	python -m venv .venv
	.\.venv\Scripts\python.exe -m pip install --upgrade pip
	.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
	make win-path-install

unix-install:
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r requirements.txt
	make unix-path-install

win-path-install:
	"$(get-location)" > .\.venv\Lib\site-packages\grenouillebot.pth

unix-path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/grenouillebot.pth &&) echo

win-run:
	.\.venv\Scripts\python.exe .\app.py

unix-run:
	.venv/bin/python3 bot/bot_application.py

win-clean:
	rm .venv

unix-clean:
	rm -rf .venv

# DATABASE
win-db-upgrade:
	.\.venv\Scripts\alembic.exe upgrade head

unix-db-upgrade:
	.venv/bin/alembic upgrade head

win-db-downgrade:
	.\.venv\Scripts\alembic.exe downgrade -1

unix-db-downgrade:
	.venv/bin/alembic downgrade -1

win-db-migrate:
	.\.venv\Scripts\alembic.exe  revision --autogenerate

unix-db-migrate:
	.venv/bin/alembic revision --autogenerate
