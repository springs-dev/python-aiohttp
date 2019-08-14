import asyncio

import argparse
from aiohttp import web

from .connections import init_connections, close_connections
from .middlewares import init_middlewares
from .routes import setup_routes


def init(loop):
    app = web.Application(loop=loop)
    app.on_startup.append(init_connections)
    app.on_startup.append(init_middlewares)
    app.on_cleanup.append(close_connections)
    setup_routes(app)
    return app


def main(run_args):
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app, **run_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=5000)
    args = parser.parse_args()
    port = int(args.port)
    run_args = {
        'port': port,
        'host': args.host,
    }
    main(run_args)
