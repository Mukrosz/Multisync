#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class PointsWidget(APIWidget):
    endpoint = "http://localhost:3000/api/points"
    interval = 15

    def __init__(self, title: str):
        super().__init__(title)
        self.add_class("widget-center-title")

    def extract_data(self, json):
        return {
            'total': json['points']['total'],
            'daily': json['points']['daily'],
            'weekly': json['points']['weekly'],
            'monthly': json['points']['monthly'],
            'streak': json['points']['streak'],
            'state': json['connectionState'],
            'uptime': json['containerUptime']
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Total: {data.get('total', 0)}\n"
            f"Daily: {data.get('daily', 0)}\n"
            f"Weekly: {data.get('weekly', 0)}\n"
            f"Monthly: {data.get('monthly', 0)}\n"
            f"Streak: {data.get('streak', 0)}\n"
            f"Connection: {data.get('state', '...')}\n"
            f"Container Uptime: {data.get('uptime', '...')}"
        )

