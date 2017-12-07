import asyncio
from asyncio import Queue

import aiohttp

from .settings import MyLogger

logger = MyLogger('crawler')


class Crawler:
    def __init__(self, urls, loop=None, max_tasks=5):
        self._urls = urls
        self._loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self._loop)
        self._queue = Queue(loop=self._loop)
        self._max_tasks = max_tasks
        self.add_urls()

        self.done = set()

    def add_urls(self):
        for url in self._urls:
            self._queue.put(url)

    def close(self):
        self._session.close()

    async def fetch(self, url):
        await self._session.get(url)
        logger.debug('get {}'.format(url))
        self.done.add(url)

    async def work(self):
        try:
            while True:
                url = await self._queue.get()
                await self.fetch(url)
                self._queue.task_done()
        except asyncio.CancelledError:
            pass

    async def crawl(self):
        works = [asyncio.Task(self.work(), loop=self._loop) for _ in range(self._max_tasks)]
        await self._queue.join()
        for w in works:
            w.cancel()
