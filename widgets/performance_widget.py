#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class PerformanceWidget(APIWidget):
    interval = 5

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(title, api_base=api_base, api_password=api_password, **kwargs)
        self.endpoint = f"{api_base}/api/performance"

    def extract_data(self, json):
        p = json.get('performance', {})
        return {
            'total'    : p.get('totalTraffic'),
            'sessions' : p.get('sessions'),
            'in'       : p.get('inTraffic'),
            'out'      : p.get('outTraffic'),
            'users'    : p.get('users')
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        total_mb = data.get('total', 0) / 1024 / 1024
        return (
            f"Total Traffic : {total_mb:.2f} MB\n"
            f"Sessions      : {data.get('sessions', 0)}\n"
            f"In Traffic    : {data.get('in', 0)}\n"
            f"Out Traffic   : {data.get('out', 0)}\n"
            f"Users         : {data.get('users', 0)}"
        )
