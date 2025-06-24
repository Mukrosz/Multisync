#!/usr/bin/env python3
"""
Synchronizer TUI Dashboard

CLI flags
---------
--host            API host (default: localhost)
--api-port        Port exposing /api/*            (default: 3000)
--metrics-port    Port exposing /metrics          (default: 3001)
--password        HTTP basic password (overrides config file)
"""

import argparse
import json
import os
import sys
from urllib.parse import urlparse

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Vertical
from textual.widgets import Footer, Header

from widgets.config_widget import ConfigWidget
from widgets.performance_widget import PerformanceWidget
from widgets.points_widget import PointsWidget
from widgets.qos_widget import QOSWidget
from widgets.status_widget import StatusWidget

# ---------------------------------------------------------------------- #
# Helpers
# ---------------------------------------------------------------------- #

def validate_server_url(host: str, port: int) -> str:
    """
    Build **http://host:port**, run a quick reachability check, and
    return the finished URL string. Exits with code 1 on any failure.
    """
    # Ensure we have a hostname
    parsed = urlparse(host if "://" in host else f"http://{host}")
    if not parsed.hostname:
        print(f"Invalid host: {host!r}")
        sys.exit(1)

    url = f"http://{parsed.hostname}:{port}"

    try:
        resp = httpx.head(url, timeout=5.0, follow_redirects=True)
        if resp.status_code == 405:  # Method Not Allowed
            resp = httpx.get(url, timeout=5.0, follow_redirects=True)
    except httpx.RequestError as e:
        print(f"Cannot reach '{url}': {e}")
        sys.exit(1)

    return url


def load_password_from_config() -> str:
    """
    Read a password from the default config.json files
    """
    cfg_path = os.path.expanduser("~/.synchronizer-cli/config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path) as f:
                return json.load(f).get("dashboardPassword", "")
        except (OSError, json.JSONDecodeError):
            pass
    return ""


# ---------------------------------------------------------------------- #
# ARG PARSER ARGS
# ---------------------------------------------------------------------- #
def make_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run the Synchronizer TUI Dashboard")
    p.add_argument("--host", default="localhost", help="API host (default: localhost)")
    p.add_argument("--api-port", type=int, default=3000, help="Port exposing /api/*")
    p.add_argument("--metrics-port", type=int, default=3001, help="Port exposing /metrics")
    p.add_argument("--password", default=None, help="Web service password")
    return p


# ---------------------------------------------------------------------- #
# Textual App
# ---------------------------------------------------------------------- #
class DashboardApp(App):
    CSS_PATH = "dashboard.css"
    TITLE = "Synchronizer Dashboard TUI"

    # Customize the bottom/footer bar with options
    COMMAND_PALETTE_DISPLAY = "Ctrl+p"
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", key_display="Ctrl+q:"),
    ]

    def __init__(
        self,
        *,
        api_base: str,
        config_bases: list[str],  # [metrics_base, api_base]
        api_password: str,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._api_base = api_base.rstrip("/")
        self._password = api_password
        self._config_bases = config_bases

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #
    def compose(self) -> ComposeResult:
        """Build the 2 × 3 grid of widgets."""
        with Vertical():
            with Grid(id="body-grid"):
                # Row 1
                yield StatusWidget(
                    "Service Status",
                    api_base=self._api_base,
                    api_password=self._password,
                )
                yield ConfigWidget(
                    "Configuration",
                    endpoints=self._config_bases,
                    api_password=self._password,
                )

                # Row 2
                yield PerformanceWidget(
                    "Performance",
                    api_base=self._api_base,
                    api_password=self._password,
                )
                yield QOSWidget(
                    "QoS Metrics",
                    api_base=self._api_base,
                    api_password=self._password,
                )
            # Row 3
            yield PointsWidget("Points",
                api_base=self._api_base,
                api_password=self._password)
        yield Footer()
# ---------------------------------------------------------------------- #
# Entrypoint
# ---------------------------------------------------------------------- #
def main() -> None:
    args = make_arg_parser().parse_args()

    # Build & validate the two base URLs we need
    api_base     = validate_server_url(args.host, args.api_port)
    metrics_base = validate_server_url(args.host, args.metrics_port)

    # Password precedence: CLI > config file
    password = args.password if args.password is not None else load_password_from_config()

    DashboardApp(
        api_base=api_base,                   # for widgets that append /api/...
        config_bases=[metrics_base, api_base],
        api_password=password,
    ).run()


if __name__ == "__main__":
    main()

