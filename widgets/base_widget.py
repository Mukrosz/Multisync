#!/usr/bin/env python3

import json
import os
from textual.widgets import Static
from textual.reactive import reactive
from httpx import AsyncClient
from textual import work

class APIWidget(Static):
    data = reactive({})
    endpoint: str = ""
    interval: int = 10

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(classes="widget-base", **kwargs)
        self.border_title = title
        self.endpoint = api_base
        self._api_password = api_password

    def on_mount(self):
        self.update_data()
        self.set_interval(self.interval, self.update_data)

    def get_client(self) -> AsyncClient:
        return AsyncClient(auth=("", self._api_password), timeout=10)

    @work(exclusive=True)
    async def update_data(self):
        try:
            async with self.get_client() as client:
                response = await client.get(self.endpoint)
                if response.status_code == 401:
                    self.data = {'error': 'Authentication failed'}
                else:
                    self.data = self.extract_data(response.json())
        except Exception as e:
            self.data = {'error': str(e)}

    def extract_data(self, json):
        return json

    def watch_data(self, data):
        self.update(self.render_content(data))

    def render_content(self, data):
        return str(data)
