from datetime import datetime
from typing import Optional

from PySide6.QtCore import QAbstractTableModel, Qt


class ChatterModel(QAbstractTableModel):
    def __init__(self, display_left=False):
        super(ChatterModel, self).__init__()
        self.chatters = []
        self.display_left = display_left

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            el = self.chatters[index.row()]
            if index.column() == 0:
                return el.ts_join.strftime('%H:%M:%S')
            elif index.column() == 1:
                if self.display_left:
                    return el.ts_left.strftime('%H:%M:%S')
                else:
                    return el.nickname
            elif index.column() == 2:
                return el.nickname
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 0 or (index == 1 and self.display_left):
                return Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def rowCount(self, index):
        return len(self.chatters)

    def columnCount(self, index):
        if self.display_left:
            return 3
        else:
            return 2

    def add(self, cme):
        for element in self.chatters:
            if element.nickname == cme.nickname:
                return

        self.chatters.append(cme)
        self.chatters.sort(key=lambda x: x.nickname)
        self.layoutChanged.emit()

    def remove(self, nickname):
        for index, element in enumerate(self.chatters):
            if element.nickname == nickname:
                el = self.chatters.pop(index)
                self.chatters.sort(key=lambda x: x.nickname)
                self.layoutChanged.emit()
                return el

        return None


class ChatterModelElement:
    nickname: str
    ts_join: datetime
    ts_left: Optional[datetime]

    def __init__(self, nickname, ts_join, ts_left=None):
        self.nickname = nickname
        self.ts_join = ts_join
        self.ts_left = ts_left
