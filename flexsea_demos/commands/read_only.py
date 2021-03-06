from time import sleep
from typing import List

from cleo import Command
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#              ReadOnlyCommand
# ============================================
class ReadOnlyCommand(Command):
    """
    Reads device data and prints it to the screen.

    read_only
        {paramFile : Yaml file with demo parameters.}
    """

    # Schema of parameters required by the demo
    required = {"ports": List, "baud_rate": int, "run_time": int}

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.run_time = 0
        self.nLoops = 0
        self.fxs = None

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the read_only demo.
        """
        setup(self, self.required, self.argument("paramFile"))
        self.nLoops = int(self.run_time / 0.1)
        for port in self.ports:
            input("Press 'ENTER' to continue...")
            device = Device(self.fxs, port, self.baud_rate)
            self._read_only(device)

    # -----
    # _read_only
    # -----
    def _read_only(self, device):
        """
        Reads FlexSEA device and prints gathered data.

        Parameters
        ----------
        device : flexsea_demos.device.Device
            Object that manages the device information and state.
        """
        for i in range(self.nLoops):
            fxu.print_loop_count(i, self.nLoops)
            sleep(0.1)
            fxu.clear_terminal()
            device.print()
        device.close()
