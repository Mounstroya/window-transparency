import subprocess
import re

MAX_OPACITY = 4294967295  # 0xFFFFFFFF


def percent_to_cardinal(percent):
    """Convert opacity percentage (0-100) to X11 cardinal value."""
    return int(MAX_OPACITY * percent / 100)


def cardinal_to_percent(cardinal):
    """Convert X11 cardinal value to opacity percentage."""
    return round(cardinal * 100 / MAX_OPACITY)


def get_active_window_id():
    """Return the ID of the currently active window."""
    result = subprocess.run(
        ["xdotool", "getactivewindow"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError("Could not get active window ID.")
    return result.stdout.strip()


def get_window_class(window_id):
    """Return the WM_CLASS of the window (app name)."""
    result = subprocess.run(
        ["xprop", "-id", window_id, "WM_CLASS"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    match = re.search(r'"([^"]+)"', result.stdout)
    return match.group(1) if match else None


def get_window_opacity(window_id):
    """
    Return current opacity percentage of a window.
    Returns 100 if no opacity property is set.
    """
    result = subprocess.run(
        ["xprop", "-id", window_id, "_NET_WM_WINDOW_OPACITY"],
        capture_output=True, text=True
    )
    match = re.search(r"= (\d+)", result.stdout)
    if match:
        return cardinal_to_percent(int(match.group(1)))
    return 100


def set_window_opacity(window_id, percent):
    """Set window opacity to a given percentage (1-100)."""
    percent = max(1, min(100, percent))
    cardinal = percent_to_cardinal(percent)
    result = subprocess.run(
        [
            "xprop", "-id", window_id,
            "-f", "_NET_WM_WINDOW_OPACITY", "32c",
            "-set", "_NET_WM_WINDOW_OPACITY",
            hex(cardinal)
        ],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Could not set opacity: {result.stderr}")


def remove_window_opacity(window_id):
    """Remove the opacity property (restore to fully opaque)."""
    subprocess.run(
        ["xprop", "-id", window_id, "-remove", "_NET_WM_WINDOW_OPACITY"],
        capture_output=True, text=True
    )


def toggle_opacity(window_id, target_percent):
    """
    Toggle between target_percent and 100%.
    If window is already at 100% (or no opacity set), apply target_percent.
    Otherwise restore to 100%.
    Returns the new opacity percentage.
    """
    current = get_window_opacity(window_id)
    if current >= 99:
        set_window_opacity(window_id, target_percent)
        return target_percent
    else:
        remove_window_opacity(window_id)
        return 100
