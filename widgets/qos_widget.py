#!/usr/bin/env python3
"""
QOSWidget
============

Polls and returns metrics relevant data from API endpoint:
    • /api/performance

"""

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from widgets.base_widget import APIWidget


def score_translate(score: int) -> int:
    """Convert API score code (0, 1, 2) → percentage (100 %, 66 %, 33 %)."""
    return (3 - score) * 100 // 3 if score in (0, 1, 2) else 0



class QOSWidget(APIWidget):
    """Displays overall QoS and sub-scores in a 4-row grid of panels."""

    interval = 5  # seconds between polls

    # ------------------------------------------------------------------ #
    # construction
    # ------------------------------------------------------------------ #
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
        payload = responses[self.endpoints[0]].get("qos", {})

        reliability  = score_translate(payload.get("reliability"))
        availability = score_translate(payload.get("availability"))
        efficiency   = score_translate(payload.get("efficiency"))
        blurbs = payload.get("ratingsBlurbs", {})
        blurbs = blurbs if blurbs else {}

        return {
            "score": (reliability + availability + efficiency) // 3,
            "reliability": reliability,
            "availability": availability,
            "efficiency": efficiency,
            "reliability_comment":   blurbs.get("reliability", ""),
            "availability_comment":  blurbs.get("availability", ""),
            "efficiency_comment":    blurbs.get("efficiency", ""),
        }

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #

    def _colorize_percent(self, value: int) -> Text:
        """Return value as colorized Text based on range."""
        if value >= 80:
            color = "green"
        elif value >= 30:
            color = "yellow"
        else:
            color = "red"
        return Text(f"{value}%", style=color)

    def _value_panel(self, title: str, value, *, width: int | None = None, show_border: bool = True) -> Panel:
        """Return a single value inside a styled, centred Rich Panel."""
        if isinstance(value, Text):
            display_value = value
        else:
            display_value = Text(str(value if value is not None else "—"))

        body = Align(
            display_value,
            align="center",
            vertical="middle",
        )        
        panel_kwargs = {}
        if width:
            panel_kwargs["expand"] = width
            panel_kwargs["width"] = width

        if title:
            panel_kwargs["title"] = f"[#6272a4]{title}[/]"
            panel_kwargs["title_align"] = "center"

        if not show_border:
            return body 

        return Panel(
            body,
            border_style = "#666666",
            **panel_kwargs
        )

    # ------------------------------------------------------------------ #
    # render method – Textual calls this automatically
    # ------------------------------------------------------------------ #
    def render_content(self, data):
        if "error" in data:
            return f"[bold red]{data['error']}[/bold red]"

        # Row 1 ─ overall score (single-column)
        row1 = self._value_panel(
            "Overall Health Score", self._colorize_percent(data.get("score", 0)) 
        )

        # Row 2 ─ reliability value + comment
        row2 = Columns(
            [
                self._value_panel("Reliability", self._colorize_percent(data.get("reliability", 0)), width=18),
                self._value_panel("", data.get("reliability_comment"), show_border=False),
            ],
            #equal=True,
            #expand=True,
        )

        # Row 3 ─ availability value + comment
        row3 = Columns(
            [
                self._value_panel("Availability", self._colorize_percent(data.get("availability", 0)), width=18),
                self._value_panel("Comment", data.get("availability_comment"), show_border=False),
            ],
            #equal=True,
            #expand=True,
        )

        # Row 4 ─ efficiency value + comment
        row4 = Columns(
            [
                self._value_panel("Efficiency", self._colorize_percent(data.get("efficiency", 0)), width=18),
                self._value_panel("Comment", data.get("efficiency_comment"), show_border=False),
            ],
            #equal=True,
            #expand=True,
        )

        # Stack rows vertically
        return Group(row1, row2, row3, row4)

