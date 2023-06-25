from sqlalchemy import Column, Integer, String
from app import db


class Move(db.Model):
    __tablename__ = "move"
    id = Column(Integer, primary_key=True)
    move_name = Column(String)
    move_class = Column(String)
    pp = Column(Integer)
    power = Column(Integer)
    priority = Column(Integer)
    accuracy = Column(Integer)
    type = Column(String)
    flavour_text = Column(String)
    short_effect = Column(String)
    long_effect = Column(String)
    effect_chance = Column(Integer)
