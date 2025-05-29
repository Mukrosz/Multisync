#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class PerformanceWidget(APIWidget):
    endpoint = "http://localhost:3000/api/performance"
    interval = 5

    def extract_data(self, json):
        p = json['performance']
        return {
            'total': p['totalTraffic'],
            'sessions': p['sessions'],
            'in': p['inTraffic'],
            'out': p['outTraffic'],
            'users': p['users']
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        total_mb = data.get('total', 0) / 1024 / 1024
        return (
            f"Total Traffic: {total_mb:.2f} MB\n"
            f"In/Out: {data.get('in', 0)} / {data.get('out', 0)}\n"
            f"Sessions: {data.get('sessions', 0)}\n"
            f"Users: {data.get('users', 0)}"
        )
