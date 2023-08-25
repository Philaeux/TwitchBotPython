from sqlalchemy.orm import Mapped, mapped_column

from bot.data.database.entity_base import BaseEntity


class KeyValueEntity(BaseEntity):
    """A bland Key-String association table

    Attributes:
        key: unique string defining a setting
        value: value of the setting
    """
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"KeyValueEntity(key={self.key!r}, value={self.value!r})"
