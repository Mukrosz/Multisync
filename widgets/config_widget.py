#!/usr/bin/env python3
"""
ConfigWidget
============

Receives two base URLs (e.g. "http://host:3001", "http://host:3000"),
Polls and return data from endpoints:
    • /metrics
    • /api/versions

polls them, and prints a concise summary.
"""

from widgets.base_widget import APIWidget


class ConfigWidget(APIWidget):
    """Display quick node summary pulled from /metrics + /api/versions."""

    def __init__(
        self,
        title: str,
        *,
        endpoints: list[str],          # [metrics_base, api_base]
        api_password: str = "",
        **kw,
    ):
        if len(endpoints) != 2:
            raise ValueError("ConfigWidget expects exactly two base endpoints (metrics, api)")
        metrics_base, api_base = endpoints

        # Build the URLs this widget will actually poll
        metrics_ep = metrics_base.rstrip("/") + "/metrics"
        versions_ep = api_base.rstrip("/") + "/api/versions"

        super().__init__(
            title,
            endpoints=[metrics_ep, versions_ep],
            api_password=api_password,
            **kw,
        )
        self.add_class("widget-base")

    # ------------------------------------------------------------------ #
    # APIWidget hooks
    # ------------------------------------------------------------------ #
    def extract_data(self, responses):
        metrics, versions = (responses[e] for e in self.endpoints)

        # bubble up any upstream errors
        for name, payload in (("metrics", metrics), ("versions", versions)):
            if "error" in payload:
                return {"error": f"{name}: {payload['error']}"}

        sync = metrics.get("synchronizer", {})
        sys = metrics.get("system", {})
        other = versions.get("versions", {})

        return {
            "sync_hash": sync.get("syncHash", "N/A"),
            "wallet": sync.get("wallet", "N/A"),
            "hostname": sys.get("hostname", "N/A"),
            "os_platform": f"{sys.get('platform', '')} {sys.get('arch', '')}".strip(),
            "cli": metrics.get("version", "N/A"),
            "docker_image": other.get("dockerImage", "N/A"),
            "container": other.get("containerImage", "N/A"),
            "reflector": other.get("reflectorVersion", "N/A"),
            "launcher": other.get("launcher", "N/A"),
        }

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def render_content(self, data):
        """Convert dict → Rich renderable; handle 'loading' & error states."""
        # 1) Error straight from extract_data
        if "error" in data:
            return f"[bold red]{data['error']}[/bold red]"

        # 2) Initial mount before any network reply
        if not data:
            return "[yellow]Loading…[/yellow]"

        # 3) Normal render
        return (
            f"Sync Name  : {data.get('sync_hash', 'N/A')}\n"
            f"Wallet     : {data.get('wallet', 'N/A')}\n"
            f"Hostname   : {data.get('hostname', 'N/A')}\n"
            f"Platform   : {data.get('os_platform', 'N/A')}\n"
            f"CLI Ver    : {data.get('cli', 'N/A')}\n"
            f"Docker Img : {data.get('docker_image', 'N/A')}\n"
            f"Container  : {data.get('container', 'N/A')}\n"
            f"Reflector  : {data.get('reflector', 'N/A')}\n"
            f"Launcher   : {data.get('launcher', 'N/A')}"
        )

