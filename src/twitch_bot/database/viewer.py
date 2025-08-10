from sqlalchemy.orm import Mapped, mapped_column

from twitch_bot.database.base import Base


class Viewer(Base):
    __tablename__ = 'viewers'

    nickname: Mapped[str] = mapped_column(primary_key=True)
    hide_tracking: Mapped[bool] = mapped_column()
