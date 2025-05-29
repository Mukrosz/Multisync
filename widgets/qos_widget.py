#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class QOSWidget(APIWidget):
    endpoint = "http://localhost:3000/api/performance"
    interval = 5

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

