import datetime
import config
from pydantic import BaseModel
from lib import async_request, errors


class SquadronModel(BaseModel):
    name: str

    ab_kpd: int
    rb_kpd: int
    sb_kpd: int

    players: list[dict]

    @classmethod
    async def from_name(cls, name: str):
        data = await async_request.get(config.SQUADRON_ENDPOINT.format(name))

        if data is None:
            raise errors.FailedToGetStats

        return cls(
            name=name,
            players=data.get('players'),
            ab_kpd=round(data.get('kpd_a')),
            rb_kpd=round(data.get('kpd_r')),
            sb_kpd=round(data.get('kpd_s'))
        )



