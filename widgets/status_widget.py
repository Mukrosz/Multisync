#!/scripts/tui/bin/python3

from widgets.base_widget import APIWidget

class StatusWidget(APIWidget):
    endpoint = "http://localhost:3000/api/status"
    interval = 10

    def extract_data(self, json):
        return {
            'status': json['serviceStatus'],
            'docker': 'Available' if json['dockerAvailable'] else 'Not Available',
            'autostart': 'Enabled' if json['autoStart'] else 'Disabled',
            'uptime': json['uptime'],
            'container': 'Running' if json['containerRunning'] else 'Stopped'
        }

    def render_content(self, data):
        if 'error' in data:
            return f"[bold red]{data['error']}[/bold red]"
        return (
            f"Status: {data.get('status', 'Loading...')}\n"
            f"Docker: {data.get('docker', 'Loading...')}\n"
            f"Autostart: {data.get('autostart', 'Loading...')}\n"
            f"Uptime: {data.get('uptime', 'Loading...')}\n"
            f"Container: {data.get('container', 'Loading...')}"
        )
