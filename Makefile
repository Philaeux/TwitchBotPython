# Dev tests without docker

install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install -r requirements.txt
	make path-install

path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/grenouillebot.pth &&) echo

run:
	.venv/bin/python3 bot/bot_application.py

clean:
	rm -rf .venv

# DATABASE

db-upgrade:
	cd bot && ../.venv/bin/alembic upgrade head

db-downgrade:
	cd bot && ../.venv/bin/alembic downgrade -1

db-migrate:
	cd bot && ../.venv/bin/alembic revision --autogenerate
