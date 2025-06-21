#!/usr/bin/env python3
"""
PerformanceWidget
============

Polls and returns performance relevant data from API endpoint:
    • /api/performance

"""

from widgets.base_widget import APIWidget

def convert_bytes(size_in_bytes):
    """Convert bytes to KB, MB, or GB, rounded to 2 decimal places."""
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024

    if size_in_bytes >= GB:
        return f"{size_in_bytes / GB:.2f} GB"
    elif size_in_bytes >= MB:
        return f"{size_in_bytes / MB:.2f} MB"
    elif size_in_bytes >= KB:
        return f"{size_in_bytes / KB:.2f} KB"
    else:
        return f"{size_in_bytes} B"


class PerformanceWidget(APIWidget):
    interval = 5

    def __init__(self, title: str, *, api_base: str, api_password: str, **kwargs):
        super().__init__(
            title,
            endpoints=f"{api_base}/api/performance",
            api_password=api_password,
            **kwargs,
        )

    # ------------------------------------------------------------------ #
    # APIWidget hooks
    # ------------------------------------------------------------------ #
    def extract_data(self, responses):
        p = responses[self.endpoints[0]].get("performance", {})
        return {
            "total": p.get("totalTraffic"),
            "sessions": p.get("sessions"),
            "in": p.get("bytesIn"),
            "out": p.get("bytesOut"),
            "users": p.get("users"),
        }

    def render_content(self, data):
        if "error" in data:
            return f"[bold red]{data['error']}[/bold red]"
        #total_mb = (data.get("total", 0) or 0) / 1024 / 1024
        return (
#            f"Total Traffic : {total_mb:.2f} MB\n"
            f"Total Traffic : {convert_bytes(data.get('total', 0))}\n"
            f"Sessions      : {data.get('sessions', 0)}\n"
            f"In Traffic    : {convert_bytes(data.get('in', 0))}\n"
            f"Out Traffic   : {convert_bytes(data.get('out', 0))}\n"
            f"Users         : {data.get('users', 0)}"
        )

