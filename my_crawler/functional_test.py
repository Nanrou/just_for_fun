import asyncio
from contextlib import contextmanager
import io
import logging
import unittest
from random import random, randint

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import pytest

from .crawl import Crawler, simple_request


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


class TestCrawler(AioHTTPTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawler = None

    def get_app(self):

        async def hello(request):
            return web.Response(text='hello world')

        async def random_num(request):
            await asyncio.sleep(random())
            return web.Response(text=request.match_info['num'])

        async def bad_request(request):
            raise web.HTTPBadRequest()

        async def timeout(request):
            await asyncio.sleep(10)
            return web.Response(text='timeout!!!')

        app = web.Application()
        app.router.add_route('GET', '/', hello)
        resource = app.router.add_resource('/num/{num}')
        resource.add_route('GET', random_num)

        app.router.add_route('GET', '/bad', bad_request)
        app.router.add_route('GET', '/timeout', timeout)

        return app

    def url_path(self, path):
        return self.server._root.human_repr() + str(path)

    def crawl(self, urls=None, *args, **kwargs):
        if self.crawler:
            self.crawler.close()
        if urls is None:
            urls = [self.server._root]
        self.crawler = Crawler(urls, *args, loop=self.loop, **kwargs)
        self.loop.run_until_complete(self.crawler.crawl())

    @unittest_run_loop
    async def test_link(self):
        req = await self.client.request('GET', '/')
        assert req.status == 200
        text = await req.text()
        assert 'hello' in text

    def test_one_link(self):
        ss = self.loop.run_until_complete(simple_request(self.server._root))
        self.assertEqual(200, ss)
        self.crawl()
        self.assertEqual(1, len(self.crawler.done))

    def test_100_links(self):
        _num = randint(50, 100)
        self.crawl([self.url_path('num/' + str(num)) for num in range(_num)])
        self.assertEqual(_num, len(self.crawler.done))

    def test_bad_request(self):
        self.crawl(self.url_path('bad'))
        self.assertEqual(1, len(self.crawler.bad_url))

    def test_timeout(self):
        self.crawl(self.url_path('timeout'))
        self.assertEqual(0, len(self.crawler.done))


if __name__ == '__main__':
    unittest.main()
