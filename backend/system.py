import random
import time
import shutil

try:
    import psutil
except ImportError:
    psutil = None

from config import is_simulation

_start_time = time.time()


def _real_stats():
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent
    disk = shutil.disk_usage("/")
    storage = round((disk.used / disk.total) * 100, 1)
    uptime = int(time.time() - psutil.boot_time())
    return cpu, mem, storage, uptime


def _simulated_stats():
    cpu = round(random.uniform(5, 35), 1)
    mem = round(random.uniform(30, 60), 1)
    storage = round(random.uniform(35, 45), 1)
    uptime = int(time.time() - _start_time)
    return cpu, mem, storage, uptime


def get_system_stats() -> dict:
    if is_simulation() or psutil is None:
        cpu, mem, storage, uptime = _simulated_stats()
    else:
        cpu, mem, storage, uptime = _real_stats()

    return {
        "cpu": cpu,
        "memory": mem,
        "storage": storage,
        "uptime": uptime,
        "network": "ONLINE",
        "simulated": is_simulation() or psutil is None,
    }