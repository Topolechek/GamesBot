from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Index, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    platform = Column(String, nullable=False)
    image = Column(String, nullable=False)

    region = relationship('Region')

    Index('ix_game_region_platform', 'region_id', 'platform')



class GamePriceHistory(Base):
    __tablename__ = 'game_price_history'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)

    game = relationship('Game', backref='price_history')

class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    code = Column(String(8), unique=True, nullable=False)
    name = Column(String(32), nullable=False)
    currency = Column(String(16), nullable=False)
