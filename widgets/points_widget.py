#!/usr/bin/env python3

from rich.align import Align
from widgets.base_widget import APIWidget
from rich.panel import Panel
from rich.columns import Columns

class PointsWidget(APIWidget):
    interval = 15

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(title, api_base=api_base, api_password=api_password, **kwargs)
        self.add_class("widget-center-title")
        self.endpoint = f"{api_base}/api/points"

    def extract_data(self, json):
        p = json.get('points', {})
        return {
            'total'      : p.get('total', 0),
            'daily'      : p.get('daily', 0),
            'weekly'     : p.get('weekly', 0),
            'monthly'    : p.get('monthly', 0),
            'streak'     : p.get('streak', 0),
            'rank'       : p.get('rank', 0),
            'multiplier' : p.get('multiplier', 0)
        }

    def render_content(self, data):
        if "error" in data:
            return f"[bold red]{data['error']}[/bold red]"

        mappings = [
            ("Total",       data.get("total", 0)),
            ("Today",       data.get("daily", 0)),
            ("This Week",   data.get("weekly", 0)),
            ("This Month",  data.get("monthly", 0)),
            ("Day Streak",  data.get("streak", 0)),
            ("Global Rank", data.get("rank", 0)),
            ("Multiplier",  data.get("multiplier", 0)),
        ]

        panels = []
        for label, value in mappings:
            centered_value = Align(str(value), align="center", vertical="middle")
            panels.append(
                Panel(
                    centered_value, 
                    title        = f"[#6272a4]{label}[/]",
                    expand       = True,
                    border_style = "#666666",
                    title_align  = "center",
                )
            )

        return Columns(panels, expand=True)
