import os
from pathlib import Path
import shutil
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication

from bot.data.database.entity_viewer import ViewerEntity
from bot.ui.chatter_model import ChatterModel, ChatterModelElement
from bot.ui.main_window import MainWindow


from sqlalchemy.orm import Session


class QtApp:
    """QT Application used to display the GUI

    Attributes:
        app: QApplication
        window: MainWindow of the QApplication
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

        self.window.actionSettings.triggered.connect(self.on_open_settings)
        self.window.actionExit.triggered.connect(self.window.close)
        self.window.chatter_join.connect(self.on_chatter_join)
        self.window.chatter_left.connect(self.on_chatter_left)
        self.window.buttonSettingsReward.clicked.connect(self.on_settings_reward)
        self.window.buttonSettingsSave.clicked.connect(self.on_settings_save)
        self.window.buttonSettingsCancel.clicked.connect(self.on_settings_cancel)
        self.window.buttonConnect.clicked.connect(self.on_connect_irc)
        self.window.buttonDisconnect.clicked.connect(lambda: self.bot.irc.disconnect())
        self.window.buttonGenerate.clicked.connect(self.compute_blog_files)

        self.chatter_in = ChatterModel()
        self.window.tableViewIn.setModel(self.chatter_in)
        self.window.tableViewIn.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_in, index, True))
        self.chatter_out = ChatterModel(display_left=True)
        self.window.tableViewOut.setModel(self.chatter_out)
        self.window.tableViewOut.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_out, index, True))
        self.chatter_hidden = ChatterModel()
        self.window.tableViewHidden.setModel(self.chatter_hidden)
        self.window.tableViewHidden.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_hidden, index, False))

        self.window.show()

    def run(self) -> None:
        """Start the QT Application and wait for closure. Process events."""
        self.app.exec()

    def on_settings_reward(self):
        if self.bot.irc.last_claimed_reward is not None:
            self.window.lineEditSoundRewardId.setText(self.bot.irc.last_claimed_reward)

    def on_open_settings(self):
        """User opens settings tab"""
        self.window.lineEditIrcNickname.setText(self.bot.settings.irc_nickname)
        self.window.lineEditIrcToken.setText(self.bot.settings.irc_token)
        self.window.lineEditIrcChannel.setText(self.bot.settings.irc_channel)
        self.window.lineEditSoundRewardId.setText(self.bot.settings.sound_reward_id)
        self.window.lineEditBlogExportPath.setText(self.bot.settings.blog_export_path)
        self.window.centralStackedWidget.setCurrentIndex(1)

    def on_settings_save(self):
        """User saves settings modifications"""
        with Session(self.bot.database.engine) as session:
            session.expire_on_commit = False
            self.bot.settings = session.merge(self.bot.settings)
            self.bot.settings.irc_nickname = self.window.lineEditIrcNickname.text()
            self.bot.settings.irc_token = self.window.lineEditIrcToken.text()
            self.bot.settings.irc_channel = self.window.lineEditIrcChannel.text()
            self.bot.settings.sound_reward_id = self.window.lineEditSoundRewardId.text()
            self.bot.settings.blog_export_path = self.window.lineEditBlogExportPath.text()
            session.commit()
        self.bot.irc.update_credentials()
        self.window.centralStackedWidget.setCurrentIndex(0)

    def on_settings_cancel(self):
        """User cancels settings modifications"""
        self.window.centralStackedWidget.setCurrentIndex(0)

    def on_connect_irc(self):
        self.window.draw_connection_status("Try")
        self.bot.irc.connection.reconnect()

    def on_chatter_join(self, nickname):
        """When a new viewer enter the room"""
        self.chatter_out.remove(nickname)
        with Session(self.bot.database.engine) as session:
            viewer = session.get(ViewerEntity, nickname)
            if viewer is not None and viewer.hide_tracking:
                self.chatter_hidden.add(ChatterModelElement(nickname, datetime.now()))
            else:
                self.chatter_in.add(ChatterModelElement(nickname, datetime.now()))

    def on_chatter_left(self, nickname):
        """When a viewer leaves the room"""
        el = self.chatter_in.remove(nickname)
        self.chatter_hidden.remove(nickname)

        with Session(self.bot.database.engine) as session:
            viewer = session.get(ViewerEntity, nickname)
            if viewer is None or viewer.hide_tracking:
                if el is None:
                    el = ChatterModelElement(nickname, datetime.now())
                    el.ts_left = datetime.now()
                    self.chatter_out.add(el)

    def on_chatter_hide(self, model, index, hide):
        el = model.remove_at_index(index.row())

        if el.ts_left is None:
            if hide:
                self.chatter_hidden.add(el)
            else:
                self.chatter_in.add(el)

        with Session(self.bot.database.engine) as session:
            viewer = session.get(ViewerEntity, el.nickname)
            if viewer is None:
                viewer = ViewerEntity(el.nickname, hide)
                session.add(viewer)
            viewer.hide_tracking = hide
            session.commit()

    def compute_blog_files(self) -> None:
        """Generates all files necessary to be displayed on a blog.

        Generate a Markdown file listing all sounds files and copy the directory of all sound files.
        The source is the running bot and the destination can be setup in the Settings file.
        """
        if getattr(sys, 'frozen', False):
            bot_sound_dir = Path(os.path.dirname(sys.executable)) / ".." / "data" / "sounds"
        elif __file__:
            bot_sound_dir = Path(os.path.dirname(__file__)) / ".." / "data" / "sounds"

        from bot.bot import Bot
        blog_root = Path(self.bot.settings.blog_export_path)

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
