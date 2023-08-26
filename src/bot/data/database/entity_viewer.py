from sqlalchemy.orm import Mapped, mapped_column

from bot.data.database.entity_base import BaseEntity


class ViewerEntity(BaseEntity):
    __tablename__ = 'viewers'

    nickname: Mapped[str] = mapped_column(primary_key=True)
    hide_tracking: Mapped[bool] = mapped_column()

    def __init__(self, nickname, hide_tracking=False):
        self.nickname = nickname
        self.hide_tracking = hide_tracking

    def __repr__(self) -> str:
        return f"ViewerEntity(nickname={self.nickname!r}, hide_tracking={self.hide_tracking!r})"
