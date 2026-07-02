from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    prediction = Column(Float, nullable=False)

    risk = Column(String, nullable=False)

    screen_time = Column(Float, nullable=False)

    conversation = Column(Float, nullable=False)

    mobility = Column(Float, nullable=False)

    dark_time = Column(Float, nullable=False)

    app_usage = Column(Float, nullable=False)
