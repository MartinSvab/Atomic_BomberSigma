_presets = {
    "sandbox": [
        ". . . . .",
        ". . . . .",
        ". . . . .",
        ". . . . .",
        ". . . . .",
    ],
    "corners": [
        ". . x . .",
        ". x . x .",
        "x . x . x",
        ". x . x .",
        ". . x . .",
    ],
    "cross": [
        ". . x . .",
        ". . x . .",
        "x x . x x",
        ". . x . .",
        ". . x . .",
    ],
    "frame": [
        "x . x . x",
        ". . x . .",
        "x x . x x",
        ". . x . .",
        "x . x . x",
    ]
}


class GridPreset:
    """
    Wraps a small symbolic pattern and can be sampled at any grid size.

    In the pattern:
      '.' means empty
      'x' means obstacle
    """

    def __init__(self, name: str):
        if name not in _presets:
            raise ValueError(f"Unknown grid preset {name!r}")

        raw_rows = _presets[name]
        # Each row is e.g. ". . x . ."  ->  [".", ".", "x", ".", "."]
        rows = [row.split() for row in raw_rows]

        if not rows:
            raise ValueError(f"Preset {name!r} has no rows")

        width = len(rows[0])
        for r in rows:
            if len(r) != width:
                raise ValueError(f"Preset {name!r} has inconsistent row lengths")

        self.name = name
        self.rows = rows          # 2D list of tokens
        self.height = len(rows)
        self.width = width

    @classmethod
    def available_names(cls) -> list[str]:
        """Just helper if you ever want to show a list of presets in a menu."""
        return list(_presets.keys())

    def sample(self, grid_width: int, grid_height: int, row: int, col: int) -> str:
        """
        Map a big grid cell (row, col) into this small pattern.
        Returns token string like "." or "x".
        """
        if self.width == 0 or self.height == 0:
            return "."

        # Scale [0, grid_height) into [0, self.height)
        src_row = (row * self.height) // grid_height
        src_col = (col * self.width) // grid_width

        # Clamp just in case
        if src_row < 0:
            src_row = 0
        elif src_row >= self.height:
            src_row = self.height - 1

        if src_col < 0:
            src_col = 0
        elif src_col >= self.width:
            src_col = self.width - 1

        return self.rows[src_row][src_col]

    def is_obstacle(self, grid_width: int, grid_height: int, row: int, col: int) -> bool:
        """Convenience wrapper for obstacle logic."""
        token = self.sample(grid_width, grid_height, row, col)
        return token.lower() == "x"
