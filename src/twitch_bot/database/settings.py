from sqlalchemy.orm import Mapped, mapped_column

from twitch_bot.database.base import Base


class Settings(Base):
    """Table for application settings. Effectively using one row"""
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(primary_key=True)

    client_id: Mapped[str] = mapped_column(default="", server_default="")
    client_secret: Mapped[str] = mapped_column(default="", server_default="")
    channel: Mapped[str] = mapped_column(default="", server_default="")

    sound_reward_id: Mapped[str] = mapped_column()
    blog_export_path: Mapped[str] = mapped_column()
