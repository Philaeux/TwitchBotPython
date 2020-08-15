import sys
import os

from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtCore import Slot, Signal, QUrl


class BotWidget(QWidget):
    """Main widget used in the application

    Attributes:
        player: sound player
        playlist: playlist of sound to run
    """
    play_signal = Signal()

    def __init__(self, bot):
        QWidget.__init__(self)
        self.bot = bot

        self.button = QPushButton("I'm a useless button :)")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

        # Connecting the signal
        self.play_signal.connect(self.play)

    @Slot()
    def play(self):
        self.player.play()

    def play_sound(self, sound_uri):
        """Queue a sound to play"""
        if self.playlist.currentIndex() == -1:
            self.playlist.clear()
            self.playlist.addMedia(QUrl.fromLocalFile(sound_uri))
            self.play_signal.emit()
        else:
            self.playlist.addMedia(QUrl.fromLocalFile(sound_uri))


class BotUI:
    """QT Application used to display the GUI

    Attributes:
        bot: main bot owning the module
        app: QT Application
        widget: Main widget used in the application
    """
    def __init__(self, bot):
        self.bot = bot

        self.app = QApplication(sys.argv)

        self.widget = BotWidget(bot)
        self.widget.resize(500, 500)
        self.widget.show()

    def run(self):
        """Start the QT Application and wait for closure"""
        self.app.exec_()
