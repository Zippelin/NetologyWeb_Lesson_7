from aiohttp import web

from config import POSTGRE_URI
from routes import setup_router
from models import db


async def init_db(app):
    await db.set_bind(POSTGRE_URI)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


async def web_app():
    app = web.Application()
    setup_router(app)

    app.cleanup_ctx.append(init_db)
    return app


