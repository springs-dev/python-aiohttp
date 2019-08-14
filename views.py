import ujson
from aiohttp import web

from .services import format_response, BODY_ERROR
from .utils import login_profile


class ProfileLoginView(web.View):
    async def post(self):
        body = await self.request.read()
        try:
            data = ujson.loads(body)
        except:
            return web.json_response(data=format_response(error=BODY_ERROR),
                                     status=400, dumps=ujson.dumps)
        profile_info = await login_profile(data, request=self.request)
        return web.json_response(data=profile_info, dumps=ujson.dumps)
