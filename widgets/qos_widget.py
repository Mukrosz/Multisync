#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class QOSWidget(APIWidget):
    interval = 5

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(title, api_base=api_base, api_password=api_password, **kwargs)
        self.endpoint = f"{api_base}/api/performance"

    def extract_data(self, json):
        return json['qos']

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Score: {data.get('score', '...')}\n"
            f"Reliability: {data.get('reliability', '...')}\n"
            f"Availability: {data.get('availability', '...')}\n"
            f"Efficiency: {data.get('efficiency', '...')}"
        )

