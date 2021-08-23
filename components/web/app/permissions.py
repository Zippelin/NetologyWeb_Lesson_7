import functools

from models import Token, User
from aiohttp import web


ISAUTHENTICATED = 1
ISOWNER = 2


def permission(level, cls=None):
    if level == ISAUTHENTICATED:
        def is_authenticated(f):
            @functools.wraps(f)
            async def decorator(self, **kwargs):
                auth_user = await __is_authenticated(self.request.headers.get('Authentication'))
                kwargs['auth_user'] = auth_user
                if auth_user:
                    return await f(self, **kwargs)
                else:
                    return web.json_response({'message': 'you must be authorized'})
            return decorator
        return is_authenticated
    elif level == ISOWNER:
        def is_owner(f):
            @functools.wraps(f)
            async def decorator(self, **kwargs):
                try:
                    entitie_id = int(self.request.match_info.get('advert_id'))
                    entitie = await cls.get(entitie_id)
                except:
                    return web.json_response({'message': 'wrong id'})
                if entitie:
                    if entitie.owner == kwargs['auth_user'].id:
                        return await f(self, **kwargs)
                    else:
                        return web.json_response({'message': 'you can modify only your own Advert'})
                else:
                    return web.json_response({'message': 'no Advert'})
            return decorator
        return is_owner


async def __is_authenticated(token):
    if token:
        token = token.split('Token ')[1]
        try:
            token = await Token.query.where(Token.key == token).gino.one()
            return await User.get(token.user)
        except:
            return False
    return False