import discord
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound

from lib.utilities.db import Base, db_session


class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    discord_id = Column(Integer, unique=True)
    locale = Column(String, default='en')

    def __repr__(self):
        rep = f'Guild({self.id=}, {self.discord_id=})'
        return rep

    @classmethod
    async def get_or_create(cls, discord_instance: discord.Guild):
        try:
            data = db_session.query(Guild). \
                filter_by(discord_id=discord_instance.id).one()
        except NoResultFound:
            obj = Guild()

            obj.discord_id = discord_instance.id

            db_session.add(obj)
            db_session.commit()

            data = db_session.query(Guild). \
                filter_by(discord_id=discord_instance.id).one()

        return data
