from configparser import ConfigParser
import os
from pathlib import Path
import shutil
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, pyqtSignal


def compute_blog_files() -> None:
    """Generates all files necessary to be displayed on a blog.

    Generate a Markdown file listing all sounds files and copy the directory of all sound files.
    The source is the running bot and the destination can be setup in the Settings file.
    """
    if getattr(sys, 'frozen', False):
        bot_sound_dir = Path(os.path.dirname(sys.executable)) / "data" / "sound"
    elif __file__:
        bot_sound_dir = Path(os.path.dirname(__file__)) / "data" / "sound"

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


class BotMainWindow(QMainWindow):
    """Main window used in the application

    Attributes:
        player: sound player
        audio_output: audio output device
        player_playlist: list of sounds queued to be played
        play_signal: QT Signal for events asking to play a sound
    """
    play_signal = pyqtSignal(bool)

    def __init__(self, ui_config: ConfigParser) -> None:
        """Constructor

        Args:
            ui_config: ConfigParser with only the [GUI] section.
        """
        QMainWindow.__init__(self)

        self.setWindowTitle("TwitchBotPython")

        # Create all widgets
        layout = QVBoxLayout()
        widget = QWidget()

        if ui_config.get("blog_export_enabled", "False") == "True":
            compute_button = QPushButton(text="Generate Blog Files")
            compute_button.clicked.connect(compute_blog_files)
            layout.addWidget(compute_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create media player elements
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)
        self.player.setAudioOutput(self.audio_output)
        self.player_playlist = []
        self.play_signal.connect(self.play)
        self.player.playbackStateChanged.connect(self.player_status_changed)
        self.player.positionChanged.connect(self.position_changed)

    def play(self) -> None:
        """Start a sound play if the player is ready and there is a sound request in the queue"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState and len(self.player_playlist) != 0:
            to_play = self.player_playlist.pop(0)
            self.player.setSource(QUrl.fromLocalFile(to_play))
            self.player.setPosition(0)
            self.player.play()

    def queue_sound(self, sound_id: str) -> None:
        """Queue a sound to play

        Args:
            sound_id: id of the sound to play
        """
        self.player_playlist.append(sound_id)
        self.play_signal.emit(True)

    def player_status_changed(self) -> None:
        """Signal that the player can play a new sound if we are stopped."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.play_signal.emit(True)

    def position_changed(self) -> None:
        """Stop player if we are at position end -24. QT6 player seems to stop before the end..."""
        if self.player.position() == 0:
            return
        elif self.player.position() + 24 == self.player.duration():
            self.player.stop()


class BotUI:
    """QT Application used to display the GUI

    Attributes:
        app: QT Application
        window: Main widget used in the application
    """

    def __init__(self, ui_config: ConfigParser) -> None:
        """Constructor.

        Args:
            ui_config: ConfigParser with only the [GUI] section.
        """
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("TwitchBotPython")

        self.window = BotMainWindow(ui_config)
        self.window.resize(300, 150)
        self.window.show()

    def run(self) -> None:
        """Start the QT Application and wait for closure. Process events."""
        self.app.exec()
