import asyncio
from asyncio import Queue
from async_timeout import timeout
from collections.abc import MutableSequence

import aiohttp

from .settings import MyLogger

logger = MyLogger('crawler')


async def simple_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp.status


class Crawler:
    def __init__(self, urls, loop=None, max_tasks=5, debug=True, request_head=None):
        if not isinstance(urls, MutableSequence):
            urls = [urls]
        self._urls = urls
        self._loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self._loop, **request_head)
        self._queue = Queue(loop=self._loop)
        self._max_tasks = max_tasks
        self.add_urls()

        if debug:
            self.debug = debug
            self.done = set()
        self.bad_url = set()

    def add_urls(self):
        for url in self._urls:
            self._queue.put_nowait(url)

    async def close(self):
        await self._session.close()

    async def scrap(self, response):
        body = await response.text()

        if response.status == 200:
            logger.info(body)
            self.scrap_detail(body)
        else:
            logger.info('status {}'.format(response.status))
            self.bad_url.add(response.url)

    def scrap_detail(self, body):  # 由具体需求决定
        pass

    async def fetch(self, url):
        try:
            with timeout(5, loop=self._loop):
                try:
                    resp = await self._session.get(url)
                    if self.debug:
                        self.done.add(url)
                        logger.debug('get {}'.format(url))
                except aiohttp.ClientError as client_error:
                    logger.warning('fail {} for {}'.format(url, client_error))
                    return
                await self.scrap(resp)
        except asyncio.TimeoutError:
            logger.warning('timeout {}'.format(url))

    async def work(self):
        try:
            while True:
                url = await self._queue.get()
                await self.fetch(url)
                self._queue.task_done()
        except asyncio.CancelledError:
            pass

    async def crawl(self):
        try:
            works = [asyncio.Task(self.work(), loop=self._loop) for _ in range(self._max_tasks)]
            await self._queue.join()
            for w in works:
                w.cancel()
        finally:
            await self.close()
