from config import is_simulation

try:
    if not is_simulation():
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    else:
        GPIO = None
except ImportError:
    GPIO = None

_pwm_channels = {}


def setup_output(pin: int):
    if GPIO:
        GPIO.setup(pin, GPIO.OUT)


def setup_input(pin: int, pull_up: bool = True):
    if GPIO:
        pull = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull)


def set_pin(pin: int, value: bool):
    if GPIO:
        GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)
    else:
        print(f"[SIM] set_pin({pin}, {value})")


def read_pin(pin: int) -> bool:
    if GPIO:
        return GPIO.input(pin) == GPIO.HIGH
    return False  # simulated buttons are read via /api/buttons/press instead


def set_pwm(pin: int, frequency: int, duty_cycle: float):
    if GPIO:
        if pin not in _pwm_channels:
            setup_output(pin)
            pwm = GPIO.PWM(pin, frequency)
            pwm.start(duty_cycle)
            _pwm_channels[pin] = pwm
        else:
            _pwm_channels[pin].ChangeDutyCycle(duty_cycle)
    else:
        print(f"[SIM] set_pwm({pin}, freq={frequency}, duty={duty_cycle})")


def cleanup():
    if GPIO:
        GPIO.cleanup()