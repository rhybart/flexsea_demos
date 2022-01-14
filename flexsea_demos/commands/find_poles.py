from time import sleep
from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#              FindPolesCommand
# ============================================
class FindPolesCommand(Command):
    """
    Finds poles on the device.

    find_poles
        {paramFile : Yaml file with demo parameters.}
    """
    # Schema of parameters required by the demo
    required = {
        "ports" : List,
        "baud_rate" : int,
    }

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.fxs = None

    # -----
    # handle
    # -----
    def handle(self):
        """
        Finds the devices' poles.
        """
        setup(self, self.required, self.argument("paramFile"))
        for port in self.ports:
            input("Press 'ENTER' to continue...")
            dev_id = fxs.open(port, self.baud_rate, 0)
            fxs.find_poles(dev_id)
