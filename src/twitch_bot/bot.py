import logging
import os
import shutil
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import requests
from PySide6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from twitch_bot.database.settings import Settings
from twitch_bot.database.viewer import Viewer
from twitch_bot.event_sub import TwitchChatListener
from twitch_bot.oauth_callback import OauthCallback
from twitch_bot.processor_sounds.sound_processor import SoundProcessor
from twitch_bot.ui.chatter_model import ChatterModel, ChatterModelElement
from twitch_bot.ui.main_window import MainWindow
from twitch_bot.utils.helpers import check_migration

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.INFO)


class Bot:
    """Root class for the bot"""

    def __init__(self) -> None:
        # Database
        file_path = Path(os.path.dirname(__file__)) / ".." / "sqlite.db"
        uri = f"sqlite+pysqlite:///{file_path}"
        check_migration(uri)
        self.engine = create_engine(uri)

        # Settings
        self.settings = None
        with Session(self.engine, expire_on_commit=False) as session:
            self.settings = session.get(Settings, "default")
            if self.settings is None:
                self.settings = Settings(key="default")
                session.add(self.settings)
                session.commit()
            session.commit()

        # Qt App
        self.qt_app = QApplication(sys.argv)
        self.qt_window = MainWindow()

        # Signals / Connect
        self.qt_window.oauth_button.clicked.connect(self.start_oauth_process)

        self.qt_window.actionSettings.triggered.connect(self.on_open_settings)
        self.qt_window.actionExit.triggered.connect(self.qt_window.close)
        self.qt_window.chatter_join.connect(self.on_chatter_join)
        self.qt_window.chatter_left.connect(self.on_chatter_left)
        self.qt_window.buttonSettingsReward.clicked.connect(self.on_settings_reward)
        self.qt_window.buttonSettingsSave.clicked.connect(self.on_settings_save)
        self.qt_window.buttonSettingsCancel.clicked.connect(self.on_settings_cancel)
        self.qt_window.buttonConnect.clicked.connect(self.on_connect_irc)
        self.qt_window.buttonGenerate.clicked.connect(self.compute_blog_files)

        self.chatter_in = ChatterModel()
        self.qt_window.tableViewIn.setModel(self.chatter_in)
        self.qt_window.tableViewIn.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_in, index, True))
        self.chatter_out = ChatterModel(display_left=True)
        self.qt_window.tableViewOut.setModel(self.chatter_out)
        self.qt_window.tableViewOut.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_out, index, True))
        self.chatter_hidden = ChatterModel()
        self.qt_window.tableViewHidden.setModel(self.chatter_hidden)
        self.qt_window.tableViewHidden.doubleClicked.connect(
            lambda index: self.on_chatter_hide(self.chatter_hidden, index, False))
        self.qt_window.show()

        # OAuth code manager
        self.oauth_code = None
        self.oauth_callback = OauthCallback()
        self.oauth_callback.oauth_code.connect(self.on_oauth_code)

        # Twitch websocket listener
        self.listener = TwitchChatListener(self)
        self.listener.new_message.connect(self.on_chat_message)
        self.listener.new_reward.connect(self.on_reward_message)

        # Processors
        self.sound_processor = SoundProcessor(self)

    def run(self):
        """Start all independent modules."""
        self.qt_app.exec()
        # self.listener.kill

    def start_oauth_process(self):
        """Open browser for streamer to login"""
        self.oauth_callback.start()
        params = {
            "client_id": self.settings.client_id,
            "redirect_uri": "http://localhost:9555",
            "response_type": "code",
            "scope": "chat:read user:read:chat"
        }
        url = requests.Request("GET", "https://id.twitch.tv/oauth2/authorize", params=params).prepare().url
        webbrowser.open(url)

    def on_oauth_code(self, code):
        self.oauth_code = code
        if self.oauth_code is not None:
            self.listener.start()

    def on_chat_message(self, user, message):
        logging.info(f"{user}: {message}")

    def on_reward_message(self, reward_id, user, message):
        logging.info(f"{reward_id} from {user}: {message}")
        self.sound_processor.process_sound(message)

    def update_settings(self, irc_nickname, irc_token, irc_channel, sound_reward_id, bloc_export_path):
        with Session(self.engine) as session:
            self.settings = session.merge(self.settings)
            self.settings.irc_nickname = irc_nickname
            self.settings.irc_token = irc_token
            self.settings.irc_channel = irc_channel
            self.settings.sound_reward_id = sound_reward_id
            self.settings.blog_export_path = bloc_export_path
            session.commit()

    def on_settings_reward(self):
        if self.irc.last_claimed_reward is not None:
            self.qt_window.lineEditSoundRewardId.setText(self.irc.last_claimed_reward)

    def on_open_settings(self):
        """User opens settings tab"""
        self.qt_window.lineEditIrcNickname.setText(self.settings.irc_nickname)
        self.qt_window.lineEditIrcToken.setText(self.settings.irc_token)
        self.qt_window.lineEditIrcChannel.setText(self.settings.irc_channel)
        self.qt_window.lineEditSoundRewardId.setText(self.settings.sound_reward_id)
        self.qt_window.lineEditBlogExportPath.setText(self.settings.blog_export_path)
        self.qt_window.centralStackedWidget.setCurrentIndex(1)

    def on_settings_save(self):
        """User saves settings modifications"""
        self.update_settings(self.qt_window.lineEditIrcNickname.text(),
                             self.qt_window.lineEditIrcToken.text(),
                             self.qt_window.lineEditIrcChannel.text(),
                             self.qt_window.lineEditSoundRewardId.text(),
                             self.qt_window.lineEditBlogExportPath.text())
        self.qt_window.centralStackedWidget.setCurrentIndex(0)

    def on_settings_cancel(self):
        """User cancels settings modifications"""
        self.qt_window.centralStackedWidget.setCurrentIndex(0)

    def on_connect_irc(self):
        self.qt_window.draw_connection_status("Try")
        self.irc.connection.reconnect()

    def on_chatter_join(self, nickname):
        """When a new viewer enter the room"""
        self.chatter_out.remove(nickname)
        with Session(self.database.engine) as session:
            viewer = session.get(Viewer, nickname)
            if viewer is not None and viewer.hide_tracking:
                self.chatter_hidden.add(ChatterModelElement(nickname, datetime.now()))
            else:
                self.chatter_in.add(ChatterModelElement(nickname, datetime.now()))

    def on_chatter_left(self, nickname):
        """When a viewer leaves the room"""
        el = self.chatter_in.remove(nickname)
        self.chatter_hidden.remove(nickname)

        with Session(self.database.engine) as session:
            viewer = session.get(Viewer, nickname)
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

        with Session(self.database.engine) as session:
            viewer = session.get(Viewer, el.nickname)
            if viewer is None:
                viewer = Viewer(el.nickname, hide)
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
        else:
            bot_sound_dir = Path(os.path.dirname(__file__)) / ".." / "data" / "sounds"

        blog_root = Path(self.settings.blog_export_path)

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
