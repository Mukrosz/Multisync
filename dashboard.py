#!/usr/bin/env python3

import os
import json
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static
from widgets.status_widget import StatusWidget
from widgets.performance_widget import PerformanceWidget
from widgets.qos_widget import QOSWidget
from widgets.points_widget import PointsWidget
from widgets.config_widget import ConfigWidget

CONFIG_PATH = os.path.expanduser("~/.synchronizer-cli/config.json")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    API_PASSWORD = config.get("dashboardPassword", "")
else:
    API_PASSWORD = ""

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
                yield StatusWidget("Service Status")
                yield ConfigWidget("Configuration", config=config)
            with Horizontal():
                yield PerformanceWidget("Performance")
                yield QOSWidget("QoS Metrics")
            with Horizontal():
                yield PointsWidget("Points")
        yield Footer()

if __name__ == "__main__":
    DashboardApp().run()
