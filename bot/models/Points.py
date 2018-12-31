from bot.database import Base
from sqlalchemy import Column, Integer, String

class UserPoints(Base):
    __tablename__ = 'user_points'

    username = Column(String, primary_key=True)
    points = Column(Integer, nullable=False, default=0, index=True)

    def __init__(self, username, points):
        self.username = username
        self.points = points
