from datetime import datetime
from typing import Optional

from PySide6.QtCore import QAbstractListModel, Qt


class ChatterModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(ChatterModel, self).__init__(*args, **kwargs)
        self.chatters = []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            el = self.chatters[index.row()]
            if el.ts_left is None:
                return f"{el.ts_join.strftime('%H:%M:%S')}   |   {el.nickname}"
            else:
                return f"{el.ts_join.strftime('%H:%M:%S')}   |   {el.ts_left.strftime('%H:%M:%S')}   |   {el.nickname}"

    def rowCount(self, index):
        return len(self.chatters)

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
                return self.chatters.pop(index)

        return None


class ChatterModelElement:
    nickname: str
    ts_join: datetime
    ts_left: Optional[datetime]

    def __init__(self, nickname, ts_join, ts_left=None):
        self.nickname = nickname
        self.ts_join = ts_join
        self.ts_left = ts_left
