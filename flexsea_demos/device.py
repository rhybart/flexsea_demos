from time import sleep

from flexsea import flexsea as flex
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu


# ============================================
#                   Device
# ============================================
class Device:
    """
    Contains and manages the actpack/exoboot information and state.
    """
    # -----
    # constructor
    # -----
    def __init__(self, fxs, port, baud_rate, **kwargs):
        # NOTE: Can fxs be passed around like this?
        self.fxs = fxs
        self.port = port
        self.baud_rate = baud_rate
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.dev_id = self.fxs.open(self.port, self.baud_rate, 0)
        self.fxs.start_streaming(self.dev_id, freq=100, log_en=True)
        sleep(0.1)
        self.app_type = self.fxs.get_app_type(self.dev_id)

        if self.app_type.value == fxe.FX_INVALID_APP.value:
            raise KeyError(f"Invalid app type: '{self.app_type.value}'")

        try:
            app_name = fxe.APP_NAMES[self.app_type.value]
        except KeyError:
            raise RuntimeError(f"Unsupported application type: {self.app_type.value}")

        print(f"Your device is an '{app_name}'", flush=True)

        self.initial_pos = self.get_pos()

    # -----
    # motor
    # -----
    def motor(self, component, value):
        """
        Sends a command to the device motor.

        Parameters
        ----------
        component : int
            A flexsea enumeration value indicating voltage, current, etc.

        value : float
            The value to send.
        """
        self.fxs.send_motor_command(self.dev_id, component, value)

    # -----
    # read
    # -----
    def read(self):
        return self.fxs.read_device(self.dev_id)

    # -----
    # print
    # -----
    def print(self, data=None):
        """
        Reads the data from the device and then prints it to the screen.
        """
        if not data:
            data = self.read()
        fxu.print_device(data, self.app_type)

    # -----
    # set_gains
    # -----
    def set_gains(self, gains):
        # Gains are, in order: kp, ki, kd, K, B & ff
        self.fxs.set_gains(self.dev_id, gains["kp"], gains["ki"], gains["kd"], gains["K"], gains["B"], gains["ff"])

    # -----
    # get_pos
    # -----
    def get_pos(self):
        return self.read().mot_ang

    # -----
    # activate_bootloader
    # -----
    def activate_bootloader(self, target):
        self.fxs.activate_bootloader(self.dev_id, target)

    # -----
    # close
    # -----
    def close(self):
        """
        Shuts down the device.
        """
        self.fxs.close(self.dev_id)
