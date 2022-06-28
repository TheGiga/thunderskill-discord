import datetime
import config
from pydantic import BaseModel
from lib import async_request, errors


class PlayerModel(BaseModel):
    nickname: str
    rank: str
    last_update: datetime.datetime

    arcade: dict
    realistic: dict
    simulator: dict

    @classmethod
    async def from_nickname(cls, nickname: str):
        data = await async_request.get(config.PLAYER_ENDPOINT.format(nickname))

        if data is None:
            raise errors.FailedToGetStats

        stats = data.get("stats")

        nickname = stats.get('nick')
        rank = stats.get('rank')
        last_update = \
            datetime.datetime.strptime(stats.get("last_stat"), '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=3)
        # had to add -3 hours because of api's shit

        return cls(
            nickname=nickname,
            rank=rank,
            last_update=last_update,
            arcade=stats.get('a'),
            realistic=stats.get('r'),
            simulator=stats.get('s')
        )
