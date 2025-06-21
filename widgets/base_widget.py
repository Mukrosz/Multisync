#!/usr/bin/env python3
"""
APIWidget
============
Base widget for asynchronous API polling.
Sets default attributes for all other widgets
"""

import asyncio
from typing import Mapping, Sequence

from httpx import AsyncClient
from textual import work
from textual.reactive import reactive
from textual.widgets import Static


class APIWidget(Static):
    """Base class for all dashboard widgets that hit an HTTP API."""

    # will hold whatever ``extract_data`` returns
    data = reactive({})

    # default refresh every N seconds – subclasses can override class attr
    interval: int = 10

    # list of endpoints after normalisation
    endpoints: list[str]

    def __init__(
        self,
        title: str,
        *,
        endpoints: str | Sequence[str],
        api_password: str,
        interval: int | None = None,
        **kwargs,
    ):
        super().__init__(classes="widget-base", **kwargs)
        self.border_title = title

        # normalise to list[str] so the rest of the code is simple
        self.endpoints = [endpoints] if isinstance(endpoints, str) else list(endpoints)

        self._api_password = api_password

        # allow caller to override the refresh cadence ad-hoc
        if interval is not None:
            self.interval = interval

    # ------------------------------------------------------------------ #
    # Textual lifecycle
    # ------------------------------------------------------------------ #
    def on_mount(self):
        # one immediate fetch + recurring timer
        self.update_data()
        self.set_interval(self.interval, self.update_data)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #
    def get_client(self) -> AsyncClient:
        """Return a pre-configured HTTPX client."""
        return AsyncClient(auth=("", self._api_password), timeout=10)

    @work(exclusive=True)
    async def update_data(self):
        """Fetch *all* configured endpoints concurrently and refresh self.data."""
        async with self.get_client() as client:
            tasks = [client.get(url) for url in self.endpoints]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        responses: dict[str, Mapping] = {}
        for url, result in zip(self.endpoints, results):
            if isinstance(result, Exception):
                # network failure etc.
                responses[url] = {"error": str(result)}
            else:
                if result.status_code == 401:
                    responses[url] = {"error": "Authentication failed"}
                else:
                    try:
                        responses[url] = result.json()
                    except ValueError:
                        responses[url] = {"error": "Invalid JSON"}

        # pass everything to subclass for domain-specific handling
        self.data = self.extract_data(responses)

    # ------------------------------------------------------------------ #
    # Hooks for subclasses
    # ------------------------------------------------------------------ #
    def extract_data(self, responses: Mapping[str, Mapping]) -> Mapping:
        """Return what is needed for rendering (default = 1st payload)."""
        # keep backward-compat: if only one endpoint, unwrap
        return next(iter(responses.values()))

    def watch_data(self, data):
        self.update(self.render_content(data))

    def render_content(self, data):
        """Convert *data* into a Rich renderable (string by default)."""
        return str(data)

