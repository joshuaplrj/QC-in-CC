"""Shared UI helpers for classical systems GUIs."""


def configure_window_geometry(root, width=1400, height=900):
    """Set a centered window size that fits the current display."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    target_width = min(width, screen_width)
    target_height = min(height, screen_height)

    x_pos = max((screen_width - target_width) // 2, 0)
    y_pos = max((screen_height - target_height) // 2, 0)

    root.geometry(f"{target_width}x{target_height}+{x_pos}+{y_pos}")
