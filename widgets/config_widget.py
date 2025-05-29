#!/usr/bin/env python3

from widgets.base_widget import Static
import socket
import platform

class ConfigWidget(Static):
    def __init__(self, title: str, config: dict):
        super().__init__(classes="widget-base")
        self.border_title = title
        self.config = config

    def on_mount(self):
        self.refresh_display()

    def refresh_display(self):
        sync_hash = self.config.get("syncHash", "N/A")
        key = self.config.get("key", "N/A")
        wallet = self.config.get("wallet", "N/A")
        hostname = socket.gethostname()
        os_platform = platform.architecture()

        content = (
            f"Sync Name: {sync_hash}\n"
            f"Sync Key: {key}\n"
            f"Wallet: {wallet}\n"
            f"Hostname: {hostname}\n"
            f"Platform: {os_platform}"
        )
        self.update(content)

