from time import sleep
from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#       TwoDevPositionControlCommand
# ============================================
class TwoDevPositionControlCommand(Command):
    """
    Runs the two devices position control demo.

    two_devices_position_control
        {paramFile : Yaml file with demo parameters.}
    """
    # Schema of parameters required by the demo
    required = {
        "ports" : List,
        "baud_rate" : int,
        "run_time" : int
    }

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.run_time = 0
        self.nLoops = 0
        self.devices = []
        self.fxs = None

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the two devices position control demo.
        """
        setup(self, self.required, self.argument("paramFile"))
        self.nLoops = int(self.run_time / 0.1)

        try:
            assert len(self.ports) == 2
        except AssertionError:
            raise AssertionError(f"Need two devices. Got: '{len(self.ports)}'")

        for i in range(2):
            self.devices.append(Device(self.fxs, self.ports[i], self.baud_rate)
            self.devices[i].set_gains(50, 3, 0, 0, 0, 0)
            self.devices[i].motor(fxe.FX_POSITION, self.devices[i].initial_position)

        self_two_devices_position_control()

        print("Turning off position control...")
        for i in range(2):
            self.devices[i].set_gains(0, 0, 0, 0, 0, 0)
            self.devices[i].motor(fxe.FX_NONE, 0)
            sleep(0.5)
            self.devices[j]..close()

    # -----
    # _two_devices_position_control
    # -----
    def _two_devices_position_control(self):
        for i in range(self.nLoops):
            sleep(0.1)
            fxu.clear_terminal()

            for j in range(2):
            cur_pos = self.devices[j].get_pos()
            pos0 = self.devices[j].initial_position

            print(f"Device {j}:\n---------\n")
            print(f"Desired:              {initial_position}")
            print(f"Measured:             {cur_pos}")
            print(f"Difference:           {cur_pos - initial_position}\n")
            self.devices[j].print()

            fxu.print_loop_count(i, self.nLoops)
