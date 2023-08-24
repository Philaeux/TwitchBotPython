#######################################
#        Windows environment          #
#######################################

## Create a virtual environment and install dependencies
win-install:
	python -m venv .wvenv
	.\.wvenv\Scripts\python.exe -m pip install --upgrade pip
	.\.wvenv\Scripts\python.exe -m pip install -r .\requirements.txt
	"$(get-location)" > .\.wvenv\Lib\site-packages\bot.pth

## Run the development files
win-run: win-gen-ui win-gen-resources
	.\.wvenv\Scripts\python.exe .\main.py

## Remove development environment
win-clean: win-build-clean
	rm -r .\.wvenv\

win-build-clean:
	rm -r .\build\
	rm -r .\dist\
	rm -r .\bundle\

# Generate UI from Qt Designer files
win-gen-ui:
	.\.wvenv\Scripts\pyside6-uic.exe ./bot/ui/ui_main_window.ui -o ./bot/ui/ui_main_window.py --absolute-imports -python-paths .

# Generate embedded resources from Qt resource file
win-gen-resources:
	.\.wvenv\Scripts\pyside6-rcc.exe ./bot/ui/resources.qrc -o ./bot/ui/resources_rc.py

# Generate database migrations
win-gen-migrations:
	.\.wvenv\Scripts\alembic.exe revision --autogenerate

## Generate a production build
win-build:
	.\.wvenv\Scripts\pyinstaller.exe --noconfirm .\TwitchBotPython.spec
	md .\bundle
	Compress-Archive -Force -Path "./dist/TwitchBotPython/" -DestinationPath "bundle/TwitchBotPython.zip"

#######################################
#          Unix environment           #
#######################################

## Create a virtual environment and install dependencies
unix-install:
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r requirements.txt
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd) > $(dir)/site-packages/d2notes.pth &&) echo

## Run the development files
unix-run: unix-gen-ui unix-gen-resources
	.venv/bin/python3 ./main.py

## Remove development environment
unix-clean: unix-build-clean
	rm -r ./.venv/

unix-build-clean:
	rm -r ./build
	rm -r ./dist
	rm -r ./bundle

# Generate UI from Qt Designer files
unix-gen-ui:
	./.venv/bin/pyside6-uic ./bot/ui/ui_main_window.ui -o ./bot/ui/ui_main_window.py --absolute-imports -python-paths .

# Generate embedded resources from Qt resource file
unix-gen-resources:
	./.venv/bin/pyside6-rcc ./bot/ui/resources.qrc -o ./bot/ui/resources_rc.py

# Generate database migrations
unix-gen-migrations:
	./.venv/bin/alembic revision --autogenerate

## Generate a production build
unix-build:
	./.venv/bin/pyinstaller --noconfirm ./TwitchBotPython.spec
