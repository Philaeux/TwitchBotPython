import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, pyqtSignal


class BotWidget(QWidget):
    """Main widget used in the application

    Attributes:
        player: sound player
        audio_output: audio output device
        player_playlist: list of sounds queued to be played
    """
    play_signal = pyqtSignal(bool)

    def __init__(self, bot):
        QWidget.__init__(self)
        self.bot = bot

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)
        self.player.setAudioOutput(self.audio_output)
        self.player_playlist = []

        self.play_signal.connect(self.play)
        self.player.playbackStateChanged.connect(self.player_status_changed)
        self.player.positionChanged.connect(self.position_changed)

    def play(self):
        """Start a sound play if the player is ready"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState and len(self.player_playlist) != 0:
            to_play = self.player_playlist.pop(0)
            self.player.setSource(QUrl.fromLocalFile(to_play))
            self.player.setPosition(0)
            self.player.play()

    def play_sound(self, sound_uri):
        """Queue a sound to play"""
        self.player_playlist.append(sound_uri)
        self.play_signal.emit(True)

    def player_status_changed(self):
        """Start a new sound if the player is not reading anymore"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.play_signal.emit(True)

    def position_changed(self):
        """Checked if we are at position end -24. QT6 player seems to stop before the end..."""
        if self.player.position() == 0:
            return
        elif self.player.position() + 24 == self.player.duration():
            self.player.stop()


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
        self.app.exec()
