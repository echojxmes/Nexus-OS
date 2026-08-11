import random
import time
from config import is_simulation

_sim_state = {"temp": 21.0, "humidity": 48.0, "pressure": 1013.0}
_bme = None

if not is_simulation():
    try:
        import board
        import adafruit_bme280.advanced as adafruit_bme280
        i2c = board.I2C()
        _bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
    except Exception as e:
        print(f"BME280 init failed, falling back to simulation: {e}")
        _bme = None


def _drift(value, spread, lo, hi):
    value += random.uniform(-spread, spread)
    return round(max(lo, min(hi, value)), 1)


def read_environment() -> dict:
    if _bme is not None:
        return {
            "temperature": round(_bme.temperature, 1),
            "humidity": round(_bme.humidity, 1),
            "pressure": round(_bme.pressure, 1),
            "simulated": False,
        }

    _sim_state["temp"] = _drift(_sim_state["temp"], 0.15, 18, 26)
    _sim_state["humidity"] = _drift(_sim_state["humidity"], 0.5, 35, 60)
    _sim_state["pressure"] = _drift(_sim_state["pressure"], 0.3, 995, 1025)

    return {
        "temperature": _sim_state["temp"],
        "humidity": _sim_state["humidity"],
        "pressure": _sim_state["pressure"],
        "simulated": True,
    }