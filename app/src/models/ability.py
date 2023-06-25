from sqlalchemy import Column, Integer, String
from app import db


class Ability(db.Model):
    __tablename__ = "ability"
    id = Column(Integer, primary_key=True)
    ability_name = Column(String)
    flavour_text_entry = Column(String)
    short_effect = Column(String)
    long_effect = Column(String)
