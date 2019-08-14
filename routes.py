from aiohttp.web import route

from .views import ProfileLoginView


routes = [
    route('POST', '/api/v1/profile/login', ProfileLoginView),
]


def setup_routes(app):
    app.add_routes(routes)
