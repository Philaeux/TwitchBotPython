# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTableView, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1326, 744)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.centralStackedWidget = QStackedWidget(self.centralwidget)
        self.centralStackedWidget.setObjectName(u"centralStackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.grid = QWidget(self.page)
        self.grid.setObjectName(u"grid")
        self.gridLayout = QGridLayout(self.grid)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableViewOut = QTableView(self.grid)
        self.tableViewOut.setObjectName(u"tableViewOut")
        self.tableViewOut.setMinimumSize(QSize(420, 0))
        self.tableViewOut.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableViewOut.setAlternatingRowColors(True)
        self.tableViewOut.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableViewOut.setCornerButtonEnabled(False)
        self.tableViewOut.horizontalHeader().setVisible(False)
        self.tableViewOut.horizontalHeader().setStretchLastSection(True)
        self.tableViewOut.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableViewOut, 2, 1, 1, 1)

        self.tableViewIn = QTableView(self.grid)
        self.tableViewIn.setObjectName(u"tableViewIn")
        self.tableViewIn.setMinimumSize(QSize(420, 0))
        self.tableViewIn.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableViewIn.setAlternatingRowColors(True)
        self.tableViewIn.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableViewIn.setCornerButtonEnabled(False)
        self.tableViewIn.horizontalHeader().setVisible(False)
        self.tableViewIn.horizontalHeader().setStretchLastSection(True)
        self.tableViewIn.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableViewIn, 2, 0, 1, 1)

        self.tableViewHidden = QTableView(self.grid)
        self.tableViewHidden.setObjectName(u"tableViewHidden")
        self.tableViewHidden.setMinimumSize(QSize(420, 0))
        self.tableViewHidden.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableViewHidden.setAlternatingRowColors(True)
        self.tableViewHidden.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableViewHidden.setCornerButtonEnabled(False)
        self.tableViewHidden.horizontalHeader().setVisible(False)
        self.tableViewHidden.horizontalHeader().setStretchLastSection(True)
        self.tableViewHidden.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableViewHidden, 2, 2, 1, 1)

        self.label = QLabel(self.grid)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.horizontalWidget = QWidget(self.grid)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.labelHeartbeat = QLabel(self.horizontalWidget)
        self.labelHeartbeat.setObjectName(u"labelHeartbeat")

        self.horizontalLayout.addWidget(self.labelHeartbeat)

        self.labelConnectionOn = QLabel(self.horizontalWidget)
        self.labelConnectionOn.setObjectName(u"labelConnectionOn")
        self.labelConnectionOn.setMinimumSize(QSize(20, 20))
        self.labelConnectionOn.setMaximumSize(QSize(20, 20))
        self.labelConnectionOn.setStyleSheet(u"background-color: rgb(0, 170, 0);")

        self.horizontalLayout.addWidget(self.labelConnectionOn)

        self.labelConnectionTry = QLabel(self.horizontalWidget)
        self.labelConnectionTry.setObjectName(u"labelConnectionTry")
        self.labelConnectionTry.setMinimumSize(QSize(20, 20))
        self.labelConnectionTry.setMaximumSize(QSize(20, 20))
        self.labelConnectionTry.setStyleSheet(u"background-color: rgb(255, 255, 0);")

        self.horizontalLayout.addWidget(self.labelConnectionTry)

        self.labelConnectionOff = QLabel(self.horizontalWidget)
        self.labelConnectionOff.setObjectName(u"labelConnectionOff")
        self.labelConnectionOff.setMinimumSize(QSize(20, 20))
        self.labelConnectionOff.setMaximumSize(QSize(20, 20))
        self.labelConnectionOff.setStyleSheet(u"background-color: rgb(255, 0, 0);")

        self.horizontalLayout.addWidget(self.labelConnectionOff)

        self.oauth_button = QPushButton(self.horizontalWidget)
        self.oauth_button.setObjectName(u"oauth_button")

        self.horizontalLayout.addWidget(self.oauth_button)

        self.buttonDisconnect = QPushButton(self.horizontalWidget)
        self.buttonDisconnect.setObjectName(u"buttonDisconnect")

        self.horizontalLayout.addWidget(self.buttonDisconnect)

        self.line = QFrame(self.horizontalWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.buttonGenerate = QPushButton(self.horizontalWidget)
        self.buttonGenerate.setObjectName(u"buttonGenerate")

        self.horizontalLayout.addWidget(self.buttonGenerate)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout.addWidget(self.horizontalWidget, 0, 0, 1, 3)

        self.label_12 = QLabel(self.grid)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.label_2 = QLabel(self.grid)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.grid)

        self.centralStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridWidget = QWidget(self.page_2)
        self.gridWidget.setObjectName(u"gridWidget")
        self.verticalLayout_4 = QVBoxLayout(self.gridWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.gridWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.lineEditClientID = QLineEdit(self.gridWidget)
        self.lineEditClientID.setObjectName(u"lineEditClientID")

        self.horizontalLayout_4.addWidget(self.lineEditClientID)

        self.label_4 = QLabel(self.gridWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.gridWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEditClientSecret = QLineEdit(self.gridWidget)
        self.lineEditClientSecret.setObjectName(u"lineEditClientSecret")
        self.lineEditClientSecret.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_5.addWidget(self.lineEditClientSecret)

        self.label_6 = QLabel(self.gridWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.gridWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.lineEditChannel = QLineEdit(self.gridWidget)
        self.lineEditChannel.setObjectName(u"lineEditChannel")

        self.horizontalLayout_6.addWidget(self.lineEditChannel)

        self.label_8 = QLabel(self.gridWidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = QLabel(self.gridWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_9)

        self.lineEditSoundRewardId = QLineEdit(self.gridWidget)
        self.lineEditSoundRewardId.setObjectName(u"lineEditSoundRewardId")

        self.horizontalLayout_7.addWidget(self.lineEditSoundRewardId)

        self.label_11 = QLabel(self.gridWidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_7.addWidget(self.label_11)

        self.buttonSettingsReward = QPushButton(self.gridWidget)
        self.buttonSettingsReward.setObjectName(u"buttonSettingsReward")

        self.horizontalLayout_7.addWidget(self.buttonSettingsReward)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_10 = QLabel(self.gridWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_10)

        self.lineEditBlogExportPath = QLineEdit(self.gridWidget)
        self.lineEditBlogExportPath.setObjectName(u"lineEditBlogExportPath")

        self.horizontalLayout_8.addWidget(self.lineEditBlogExportPath)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)

        self.buttonSettingsSave = QPushButton(self.gridWidget)
        self.buttonSettingsSave.setObjectName(u"buttonSettingsSave")

        self.horizontalLayout_9.addWidget(self.buttonSettingsSave)

        self.buttonSettingsCancel = QPushButton(self.gridWidget)
        self.buttonSettingsCancel.setObjectName(u"buttonSettingsCancel")

        self.horizontalLayout_9.addWidget(self.buttonSettingsCancel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.gridWidget)

        self.centralStackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.centralStackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1326, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.centralStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TwitchBotPython", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Chatters In</span></p></body></html>", None))
        self.labelHeartbeat.setText("")
        self.labelConnectionOn.setText("")
        self.labelConnectionTry.setText("")
        self.labelConnectionOff.setText("")
        self.oauth_button.setText(QCoreApplication.translate("MainWindow", u"Start OAuth", None))
        self.buttonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.buttonGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate Blog Files", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Hidden</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Chatters Out</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Client ID</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Bot Client ID, get one <a href=\"https://dev.twitch.tv/console/apps\"><span style=\" text-decoration: underline; color:#99ebff;\">in the twitch console.</span></a></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Client Secret</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Associated Client Secret.</p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Twitch Channel</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Chat to listen to.", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Sound Reward ID</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Reward that activate the soundboard.", None))
        self.buttonSettingsReward.setText(QCoreApplication.translate("MainWindow", u"Extract ID of latest used Reward", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Blog Export Path</span></p></body></html>", None))
        self.buttonSettingsSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.buttonSettingsCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

