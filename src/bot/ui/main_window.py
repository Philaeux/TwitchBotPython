from PySide6.QtCore import Signal, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QMainWindow

from bot.ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Application main window that is seeded with the generated class from .ui file"""

    play_signal = Signal(bool)
    chatter_join = Signal(str)
    chatter_left = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Create media player elements
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)
        self.player.setAudioOutput(self.audio_output)
        self.player_playlist = []
        self.play_signal.connect(self.play)
        self.player.playbackStateChanged.connect(self.player_status_changed)
        self.player.positionChanged.connect(self.position_changed)

        self.centralStackedWidget.setCurrentIndex(0)

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
