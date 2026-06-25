from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    password_hash = Column(String)

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    prediction = Column(Float)

    risk = Column(String)

    screen_time = Column(Float)

    conversation = Column(Float)

    mobility = Column(Float)

    dark_time = Column(Float)

    app_usage = Column(Float)
