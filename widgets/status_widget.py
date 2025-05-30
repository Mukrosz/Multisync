#!/usr/bin/env python3

from widgets.base_widget import APIWidget

class StatusWidget(APIWidget):
    interval = 10

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(title, api_base=api_base, api_password=api_password, **kwargs)
        self.endpoint = f"{api_base}/api/status"

    def extract_data(self, json):
        return {
            'status'         : 'Running' if json.get('serviceStatus') == 'running' else 'Not Running',
            'docker'         : 'Available' if json.get('dockerAvailable') else 'Not Available',
            'autostart'      : 'Enabled' if json.get('autoStart') else 'Not Enabled',
            'uptime'         : json.get('uptime', 'N/A'),
            'image_updates'  : json.get('imageUpdates', {}).get('available', 'N/A'),
            'last_checked'   : json.get('imageUpdates', {}).get('lastChecked', 'N/A')
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Service Status : {data.get('status', 'Loading...')}\n"
            f"Docker Status  : {data.get('docker', 'Loading...')}\n"
            f"Auto-start     : {data.get('autostart', 'Loading...')}\n"
            f"Uptime         : {data.get('uptime', 'Loading...')}\n"
            f"Image Updates  : {data.get('image_updates', 'Loading...')}\n"
            f"Last Checked   : {data.get('last_checked', 'Loading...')}"
        )
