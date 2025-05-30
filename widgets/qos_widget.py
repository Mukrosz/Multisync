#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class QOSWidget(APIWidget):
    interval = 5

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(title, api_base=api_base, api_password=api_password, **kwargs)
        self.endpoint = f"{api_base}/api/performance"

    def extract_data(self, json):
        qos = json.get('qos', {})
        return {
            'score'        : qos.get('score'),
            'reliability'  : qos.get('reliability'),
            'availability' : qos.get('availability'),
            'efficiency'   : qos.get('efficiency'),
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Score        : {data.get('score', 'Loading...')}\n"
            f"Reliability  : {data.get('reliability', 'Loading...')}\n"
            f"Availability : {data.get('availability', 'Loading...')}\n"
            f"Efficiency   : {data.get('efficiency', 'Loading...')}\n"
        )

