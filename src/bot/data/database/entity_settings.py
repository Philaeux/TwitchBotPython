from sqlalchemy.orm import Mapped, mapped_column

from bot.data.database.entity_base import BaseEntity


class SettingsEntity(BaseEntity):
    """Table for application settings. Effectively using one row

    Attributes:
        key: unique string defining a setting
        irc_nickname: value of the setting
    """
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(primary_key=True)
    irc_nickname: Mapped[str] = mapped_column()
    irc_token: Mapped[str] = mapped_column()
    irc_channel: Mapped[str] = mapped_column()
    sound_reward_id: Mapped[str] = mapped_column()
    blog_export_path: Mapped[str] = mapped_column()

    def __init__(self, key, irc_nickname="", irc_token="", irc_channel="twitch", sound_reward_id="", blog_export_path=""):
        self.key = key
        self.irc_nickname = irc_nickname
        self.irc_token = irc_token
        self.irc_channel = irc_channel
        self.sound_reward_id = sound_reward_id
        self.blog_export_path = blog_export_path

    def __repr__(self) -> str:
        return f"SettingsEntity(key={self.key!r}, irc_nickname={self.irc_nickname!r}, irc_channel={self.irc_channel})"
