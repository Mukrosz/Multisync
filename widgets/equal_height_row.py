# widgets/equal_height_row.py
from __future__ import annotations

from textual import events
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive


class EqualHeightRow(Horizontal):
    """
    A Horizontal container that

    • measures its tallest visible child,
    • fixes *its own* height to that value, and
    • assigns every child the same height,

    so borders line-up and no blank areas appear.
    """

    _row_height: reactive[int] = reactive(0, layout=True)

    class _Sync(Message): """Internal debounce message."""

    # ─────────────────── life-cycle hooks ────────────────────
    def on_mount(self) -> None:
        self.post_message(self._Sync())

    def on_post_layout(self, _) -> None:
        self.post_message(self._Sync())

    def on_resize(self, _: events.Resize) -> None:
        self.post_message(self._Sync())

    # ─────────────────── sync handler ────────────────────────
    def handle__sync(self, _: _Sync) -> None:
        self._sync_heights()

    # ─────────────────── helpers ─────────────────────────────
    def _measure(self, child) -> int:
        region = getattr(child, "content_region", None)
        if region:                                   # already laid out
            return region.size.height
        width = self.size.width if self.has_size else 0
        return child.get_content_height(self.app.console, width)

    def _sync_heights(self) -> None:
        tallest = max(
            (self._measure(c) for c in self.children if c.display), default=0
        )
        if not tallest or tallest == self._row_height:
            return

        self._row_height = tallest

        # 🔒 1. Lock the row to the exact height
        self.styles.height = tallest

        # 🔒 2. Stretch every child to fill the row
        for c in self.children:
            c.styles.height = tallest

        # ♻️ 3. Trigger a relayout
        self.refresh(layout=True)

