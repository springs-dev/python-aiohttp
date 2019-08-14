from aiohttp import web

from .conf import settings
from .helpers import REASON_BAD_TOKEN, REASON_NO_CSRF_COOKIE, _compare_salted_tokens, csrf_logger


@web.middleware
async def csrf_middleware(request, handler):
    func = getattr(handler, request.method.lower(), handler)
    if request.method not in {'GET', 'HEAD', 'OPTIONS', 'TRACE'} and \
            not getattr(func, 'csrf_exempt', False):
        try:
            csrf_token = request.cookies[settings.CSRF_COOKIE_NAME]
        except KeyError:
            csrf_token = None

        if not csrf_token:
            csrf_logger.error(
                'cookie csrf_token is empty',
                extra={
                    'cookies': dict(request.cookies),
                    'headers': dict(request.headers),
                }
            )
            return web.HTTPForbidden(text=REASON_NO_CSRF_COOKIE)

        request_csrf_token = request.headers.get(settings.CSRF_HEADER_NAME, '')
        if not request_csrf_token or not _compare_salted_tokens(request_csrf_token, csrf_token):
            csrf_logger.error(
                'cookie csrf_token is not equal to header csrf_token',
                extra={
                    'cookies': dict(request.cookies),
                    'headers': dict(request.headers),
                }
            )
            return web.HTTPForbidden(text=REASON_BAD_TOKEN)
    return await handler(request)


async def init_middlewares(app):
    app.middlewares.append(csrf_middleware)
