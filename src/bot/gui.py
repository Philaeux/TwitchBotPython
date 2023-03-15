import sys

from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QComboBox
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

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

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
        self.app.setApplicationName("TwitchBotPython")

        self.widget = BotWidget(bot)
        self.widget.resize(300, 150)
        self.widget.show()

    def run(self):
        """Start the QT Application and wait for closure"""
        self.app.exec_()
