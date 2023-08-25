from configparser import ConfigParser
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication

from bot.ui.chatter_model import ChatterModel, ChatterModelElement
from bot.ui.main_window import MainWindow


class QtApp:
    """QT Application used to display the GUI

    Attributes:
        app: QT Application
        window: Main widget used in the application
    """

    def __init__(self, bot) -> None:
        """Constructor.

        Args:
            ui_config: ConfigParser with only the [GUI] section.
        """
        self.bot = bot
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

        self.window.actionSettings.triggered.connect(self.on_open_settings)
        self.window.actionExit.triggered.connect(self.window.close)
        self.window.chatter_join.connect(self.on_chatter_join)
        self.window.chatter_left.connect(self.on_chatter_left)
        self.window.buttonGenerate.clicked.connect(self.compute_blog_files)
        self.window.buttonSettingsSave.clicked.connect(self.on_settings_save)
        self.window.buttonSettingsCancel.clicked.connect(self.on_settings_cancel)

        self.chatter_in = ChatterModel()
        self.window.tableViewIn.setModel(self.chatter_in)
        self.chatter_out = ChatterModel(display_left=True)
        self.window.tableViewOut.setModel(self.chatter_out)

        self.window.show()

    def run(self) -> None:
        """Start the QT Application and wait for closure. Process events."""
        self.app.exec()

    def on_open_settings(self):
        self.window.centralStackedWidget.setCurrentIndex(1)

    def on_settings_save(self):
        """User saves settings modifications"""
        for ch in self.bot.irc.channels.values():
            print(ch)
            for user in ch.users():
                print(user)
        self.window.centralStackedWidget.setCurrentIndex(0)

    def on_settings_cancel(self):
        """User cancels settings modifications"""
        self.window.centralStackedWidget.setCurrentIndex(0)

    def on_chatter_join(self, nickname):
        self.chatter_out.remove(nickname)
        self.chatter_in.add(ChatterModelElement(nickname, datetime.now()))

    def on_chatter_left(self, nickname):
        el = self.chatter_in.remove(nickname)
        if el is None:
            el = ChatterModelElement(nickname, datetime.now())
        el.ts_left = datetime.now()
        self.chatter_out.add(el)

    def compute_blog_files(self) -> None:
        """Generates all files necessary to be displayed on a blog.

        Generate a Markdown file listing all sounds files and copy the directory of all sound files.
        The source is the running bot and the destination can be setup in the Settings file.
        """
        if getattr(sys, 'frozen', False):
            bot_sound_dir = Path(os.path.dirname(sys.executable)) / ".." / "data" / "sound"
        elif __file__:
            bot_sound_dir = Path(os.path.dirname(__file__)) / ".." / "data" / "sound"

        from bot.bot import Bot
        blog_root = Path(Bot().config["GUI"].get("blog_path", "C:/"))

        blog_list_file = blog_root / "sounds.md"
        blog_sound_dir = blog_root / "assets" / "sounds"

        # Copy all sounds file to blog
        if blog_sound_dir.exists():
            shutil.rmtree(blog_sound_dir)
            shutil.copytree(bot_sound_dir, blog_sound_dir)

        # Generate new blog files
        if blog_list_file.exists():
            blog_list_file.unlink()
        with open(blog_list_file, "a") as file_descriptor:
            file_descriptor.write("---\n")
            file_descriptor.write("layout: post\n")
            file_descriptor.write("title: Sounds available in Stream\n")
            file_descriptor.write("---\n")
            file_descriptor.write("Use the name to start a sound as a message of the \"Play Sound\" reward. \n")
            file_descriptor.write("\n")

            # Navigation Table
            for root, dirs, files in os.walk(bot_sound_dir, topdown=False):
                if Path(root) == bot_sound_dir:
                    continue
                section = os.path.basename(Path(root))
                section_pretty = section.replace("_", " ").title()
                file_descriptor.write("* [" + section_pretty + "](#" + section + ")\n")
            file_descriptor.write("\n")

            # All files
            for root, dirs, files in os.walk(bot_sound_dir, topdown=False):
                if Path(root) == bot_sound_dir:
                    continue
                section = os.path.basename(Path(root))
                section_pretty = section.replace("_", " ").title()
                file_descriptor.write("\n### " + section_pretty + "  <a name=\"" + section + "\"></a>\n\n")
                for name in files:
                    if name[-5:] != ".opus":
                        continue
                    file_descriptor.write("* &nbsp; <audio controls preload=\"none\"><source src=\"\\assets\\sounds\\"
                                          + section + "\\" + name + "\" type=\"audio/ogg; codecs=opus\"></audio>&nbsp; "
                                          + name[:-5].replace("_", " ") + "\n")
                file_descriptor.write("<a href=\"#\" class=\"backlogo\">&#x25B2;</a>\n")
