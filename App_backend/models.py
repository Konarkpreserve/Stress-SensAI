from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from database import Base

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

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