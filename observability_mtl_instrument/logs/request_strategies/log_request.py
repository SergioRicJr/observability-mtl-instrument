import asyncio

import httpx
import requests

from observability_mtl_instrument.logs.request_strategies.log_request_interface import (
    LogRequestInterface,
)


class LogRequest(LogRequestInterface):
    def __init__(self, loki_url, data, headers) -> None:
        self.loki_url = loki_url
        self.data = data
        self.headers = headers

    def make_request(self):
        requests.post(self.loki_url, json=self.data, headers=self.headers)


class LogRequestAsync(LogRequestInterface):
    def __init__(self, loki_url, data, headers) -> None:
        self.loki_url = loki_url
        self.data = data
        self.headers = headers

    def make_request(self):
        asyncio.create_task(self.create_request_coroutine())

    async def create_request_coroutine(self):
        async with httpx.AsyncClient() as client:
            await client.post(
                self.loki_url, json=self.data, headers=self.headers
            )
