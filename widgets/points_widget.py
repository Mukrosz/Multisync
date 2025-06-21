#!/usr/bin/env python3
"""
PointsWidget
============

Polls and returns points relevant data from API endpoint:
    • /api/points

"""

from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel

from widgets.base_widget import APIWidget


class PointsWidget(APIWidget):
    interval = 15

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(
            title,
            endpoints=f"{api_base}/api/points",
            api_password=api_password,
            **kwargs,
        )
        self.add_class("widget-center-title")

    # ------------------------------------------------------------------ #
    # APIWidget hooks
    # ------------------------------------------------------------------ #
    def extract_data(self, responses):
        performance = responses[self.endpoints[0]]
        points = performance.get("points", {})
        return {
            "life_total": performance.get("walletLifePoints", 0),
            "session_total": performance.get("syncLifePoints", 0),
            "rank": points.get("rank", 0),
            "multiplier": points.get("multiplier", 0),
        }

    def render_content(self, data):
        if "error" in data:
            return f"[bold red]{data['error']}[/bold red]"

        mappings = [
            ("Life Total", data.get("life_total", 0)),
            ("Session Total", data.get("session_total", 0)),
            ("Global Rank", data.get("rank", 0)),
            ("Multiplier", data.get("multiplier", 0)),
        ]

        panels = []
        for label, value in mappings:
            centered_value = Align(str(value), align="center", vertical="middle")
            panels.append(
                Panel(
                    centered_value,
                    title=f"[#6272a4]{label}[/]",
                    expand=True,
                    border_style="#666666",
                    title_align="center",
                )
            )

        return Columns(panels, expand=True)

