import asyncio
from contextlib import contextmanager
import io
import socket
import logging
import unittest

from aiohttp import ClientError, web
import pytest

from .crawl import Crawler


@contextmanager
def capture_logging():
    logger = logging.getLogger('crawler')
    level = logger.level
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(io.StringIO)
    logger.addHandler(handler)

    class Messages:
        def __contains__(self, item):
            return item in handler.stream.getvalue()

        def __repr__(self):
            return repr(handler.stream.getvalue())

    try:
        yield Messages()
    finally:
        logger.removeHandler(handler)
        logger.setLevel(level)


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        def close_loop():
            self.loop.stop()
            self.loop.run_forever()
            self.loop.close()

        self.addCleanup(close_loop)

        self.port = self._find_unused_port()
        self.app_url = 'http://127.0.0.1:{}'.format(self.port)
        self.app = self.loop.run_until_complete(self._create_server())
        self.crawler = None

    @staticmethod
    def _find_unused_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    async def _create_server(self):
        app = web.Application(loop=self.loop)
        handler_factory = app.make_handler(debug=True)
        srv = await self.loop.create_server(
            handler_factory, '127.0.0.1', self.port
        )

        self.addCleanup(srv.close())
        self.addCleanup(lambda: self.loop.run_until_complete(
            srv.wait_closed()
        ))
        self.addCleanup(lambda: self.loop.run_until_complete(
            app.shutdown()
        ))
        self.addCleanup(lambda: self.loop.run_until_complete(
            handler_factory.shutdown(60.00)
        ))
        self.addCleanup(lambda: self.loop.run_until_complete(
            app.cleanup()
        ))
        return app

    def add_handler(self, url, handler):
        self.app.router.add_route('GET', url, handler)

    def add_page(self, url='/', links=None, body=None, content_type=None):
        if not body:
            text = ''.join('<a href="{}"></a>'.format(link) for link in links or [])
            body = text.encode('utf-8')

        if content_type is None:
            content_type = 'text/html; charset=utf-8'

        async def handler(req):
            await req.read()
            return web.Response(body=body, headers=[('CONTENT-TYPE', content_type)])

        self.add_handler(url, handler)
        return self.app_url + url

    def add_redirect(self, url, link):
        async def handler(_):
            raise web.HTTPFound(link)

        self.add_handler(url, handler)
        return self.app_url + url

    def assertDoneCount(self, n):
        pass

    def assertStat(self, stat_index=0, **kwargs):
        pass

    def crawl(self, urls=None, *args, **kwargs):
        if self.crawler:
            self.crawler.close()
        if urls is None:
            urls = [self.app_url]
        self.crawler = Crawler(urls, *args, loop=self.loop, **kwargs)
        self.addCleanup(self.crawler.close())
        self.loop.run_until_complete(self.crawler.crawl())

    def test_link(self):
        self.add_page('/', ['/foo'])
        self.crawl()
        self.assertEqual(1, len(self.crawler.done))


if __name__ == '__main__':
    unittest.main()

