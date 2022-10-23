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

        self.out_combo = QComboBox()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.out_combo)
        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        service = self.player.service()
        if service:
            out = service.requestControl("org.qt-project.qt.audiooutputselectorcontrol/5.0")
            if out:
                for device in out.availableOutputs():
                    self.out_combo.addItem(device, device)
                self.out_combo.setCurrentText("@device:cm:{E0F158E1-CB04-11D0-BD4E-00A0C911CE86}\wave:{4885BCE7-002C-400B-9D99-9AE3A0F3B7CF}")
                out.setActiveOutput("@device:cm:{E0F158E1-CB04-11D0-BD4E-00A0C911CE86}\wave:{4885BCE7-002C-400B-9D99-9AE3A0F3B7CF}")
                service.releaseControl(out)
        self.player.setVolume(100)
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)

        self.out_combo.currentIndexChanged.connect(self.out_device_changed)
        self.play_signal.connect(self.play)

    def out_device_changed(self, idx):
        device = self.out_combo.itemData(idx)
        service = self.player.service()
        if service:
            out = service.requestControl("org.qt-project.qt.audiooutputselectorcontrol/5.0")
            if out:
                out.setActiveOutput(device)
                service.releaseControl(out)

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
