"""Utilities for future stage modeling and projection mapping."""


class Stage:
    """Placeholder representation of a stage with basic geometry."""

    def __init__(self, width: float = 10.0, depth: float = 5.0) -> None:
        self.width = width
        self.depth = depth

    def area(self) -> float:
        """Return the floor area of the stage."""
        return self.width * self.depth

    def __repr__(self) -> str:
        return f"Stage(width={self.width}, depth={self.depth})"
