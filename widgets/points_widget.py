#!/usr/bin/env python3

from widgets.base_widget import APIWidget

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
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Total       : {data.get('total', 0)}\n"
            f"Today       : {data.get('daily', 0)}\n"
            f"This Week   : {data.get('weekly', 0)}\n"
            f"This Month  : {data.get('monthly', 0)}\n"
            f"Day Streak  : {data.get('streak', 0)}\n"
            f"Global Rank : {data.get('rank', 0)}\n"
            f"Multiplier  : {data.get('multiplier', 0)}"
        )

