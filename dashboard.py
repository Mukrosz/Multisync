#!/usr/bin/env python3

import argparse
import json
import os
import sys
import httpx
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static
from urllib.parse import urlparse
from widgets.status_widget import StatusWidget
from widgets.performance_widget import PerformanceWidget
from widgets.qos_widget import QOSWidget
from widgets.points_widget import PointsWidget
from widgets.config_widget import ConfigWidget

def validate_server_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        print(f"Invalid URL format: '{url}'\n    Must start with http:// or https://")
        sys.exit(1)

    try:
        resp = httpx.head(url, timeout=5.0, follow_redirects=True)
        # some servers don’t support HEAD – if you get Method Not Allowed, try GET
        if resp.status_code == 405:
            resp = httpx.get(url, timeout=5.0, follow_redirects=True)
    except httpx.RequestError as e:
        print(f"Cannot reach '{url}': {e}")
        sys.exit(1)

CONFIG_PATH = os.path.expanduser("~/.synchronizer-cli/config.json")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    API_PASSWORD = config.get("dashboardPassword", "")
else:
    API_PASSWORD = ""

parser = argparse.ArgumentParser(description="Run the Synchronizer TUI Dashboard")
parser.add_argument("--server", "--s",
                    type    = str,
                    default = "http://localhost:3000", 
                    help    = "Set API server base URL"
)
args = parser.parse_args()
API_BASE = args.server
validate_server_url(API_BASE)

class DashboardApp(App):
    CSS_PATH = "dashboard.css"
    TITLE = "Synchronizer Dashboard TUI"

    def compose(self) -> ComposeResult:
        if not API_PASSWORD:
            yield Static("[bold red]Error: dashboardPassword not found in config[/bold red]")
            return

        yield Header()
        with Vertical():
            with Horizontal():
                yield StatusWidget("Service Status", api_base=API_BASE, api_password=API_PASSWORD)
                yield ConfigWidget("Configuration", config=config)
            with Horizontal():
                yield PerformanceWidget("Performance", api_base=API_BASE, api_password=API_PASSWORD)
                yield QOSWidget("QoS Metrics", api_base=API_BASE, api_password=API_PASSWORD) 
            with Horizontal():
                yield PointsWidget("Points", api_base=API_BASE, api_password=API_PASSWORD)
        yield Footer()

if __name__ == "__main__":
    DashboardApp().run()
