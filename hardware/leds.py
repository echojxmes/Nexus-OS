from config import is_simulation

_current_mode = "OFF"
_pixels = None
LED_COUNT = 30
LED_PIN = 18  # GPIO18, PWM-capable — matches the 74AHCT125 data line

MODES = {
    "OFF": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "BLUE": (0, 80, 255),
    "PURPLE": (140, 0, 200),
    "NEXUS": (0, 200, 180),
}

if not is_simulation():
    try:
        import board
        import neopixel
        _pixels = neopixel.NeoPixel(board.D18, LED_COUNT, auto_write=False, pixel_order=neopixel.GRB)
    except Exception as e:
        print(f"WS2812B init failed, falling back to simulation: {e}")
        _pixels = None


def set_mode(mode: str) -> dict:
    global _current_mode
    mode = mode.upper()

    if mode == "RAINBOW":
        _current_mode = mode
        if _pixels:
            _rainbow_cycle()
        else:
            print("[SIM] LEDs -> RAINBOW")
        return {"mode": _current_mode}

    if mode not in MODES:
        return {"error": f"unknown mode '{mode}'", "mode": _current_mode}

    _current_mode = mode
    color = MODES[mode]

    if _pixels:
        _pixels.fill(color)
        _pixels.show()
    else:
        print(f"[SIM] LEDs -> {mode} {color}")

    return {"mode": _current_mode}


def get_mode() -> dict:
    return {"mode": _current_mode}


def _rainbow_cycle():
    # placeholder — real HSV wheel cycling goes here once the strip is wired up
    if _pixels:
        _pixels.fill((100, 0, 200))
        _pixels.show()