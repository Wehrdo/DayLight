import time
import pigpio
from typing import Optional


class PiManager:
    def __init__(self, ip_addr: str):
        self.ip_addr = ip_addr
        self.gpio: Optional[pigpio.pi] = None

    def __enter__(self) -> pigpio.pi:
        print("Attemting to connect to pi...")
        self.gpio = pigpio.pi(self.ip_addr)
        if not self.gpio.connected:
            raise Exception(f"Could not connect to pi at {self.ip_addr}")
        print("Connected!")
        return self.gpio

    # Release resources
    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Temporarily disable exceptions
        pigpio.exceptions = False

        if self.gpio is not None and self.gpio.connected:
            self.gpio.stop()

        # Re-enable exceptions
        pigpio.exceptions = True


class Light:
    def __init__(self, gpio: pigpio.pi):
        self.pi = gpio

        # Broadcom numbering of pins
        self.PIN_Y = 18
        self.PIN_W1 = 17
        self.PIN_W2 = 27
        # For convenience
        self.all_pins = [self.PIN_Y, self.PIN_W1, self.PIN_W2]
        self.pi.managed_pins = self.all_pins

        # Range for PWM
        self.range = 1024

        # Setup PWM
        for pin in self.all_pins:
            status = self.pi.set_PWM_dutycycle(pin, 0)
            if status != 0:
                print(f"Could not enable PWM for pin {pin}")
                continue
            self.pi.set_PWM_frequency(pin, 10000)
            self.pi.set_PWM_range(pin, self.range)

    def setNormalized(self, pin: int, value: float):
        """
        Sets the PWM duty cycle of pin to value, in range [0, 1]
        """
        scaled = value * self.range
        clamped = int(min(max(0, scaled), self.range))
        self.pi.set_PWM_dutycycle(pin, clamped)

    def setYellow(self, value: float):
        self.setNormalized(self.PIN_Y, value)

    def setWhite(self, value: float):
        self.setNormalized(self.PIN_W1, value)
        self.setNormalized(self.PIN_W2, value)


if __name__ == "__main__":
    with PiManager("192.168.254.21") as gpio:
        light = Light(gpio)
        for i in range(1000):
            light.setYellow(i / 1000)
            light.setWhite(1 - i / 1000)
            time.sleep(0.1)
