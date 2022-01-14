from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#              BootloaderCommand
# ============================================
class BootloaderCommand(Command):
    """
    Runs the bootloader check.

    bootloader
        {paramFile : Yaml file with demo parameters.}
    """
    # Schema of parameters required by the demo
    required = {
        "ports" : List,
        "baud_rate" : int,
        "target" : str,
    }

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.target = ""
        self.fxs = None

        self.targets = {
            "Habs": {"id": 0, "name": "Habsolute"},
            "Reg": {"id": 1, "name": "Regulate"},
            "Exe": {"id": 2, "name": "Execute"},
            "Mn": {"id": 3, "name": "Manage"},
            "BT121": {"id": 4, "name": "Bluetooth"},
            "XBee": {"id": 5, "name": "XBee"},
        }

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the bootloader demo.
        """
        setup(self, self.required, self.argument("paramFile"))
        for port in self.ports:
            device = Device(self.fxs, port, self.baud_rate)
            self._bootloader(device)
            device..close()

    # -----
    # _bootloader
    # -----
    def _bootloader(self, device):
        print(f"Activating {TARGETS[self.target]['name']} bootloader", flush=True)
        wait_step = 1
        state = fxe.FX_FAILURE.value
        timeout = self.run_time

        while timeout > 0 and state != fxe.FX_SUCCESS.value:
            if timeout % 5 == 0:
                print("Sending signal to target device", flush=True)
                try:
                    device.activate_bootloader(self.targets[self.target]["id"])
                except (IOError, ValueError):
                    pass
            print(f"Waiting for response from target ({timeout}s)", flush=True)
            sleep(wait_step)
            timeout -= wait_step
            try:
                state = fxs.is_bootloader_activated(device.dev_id)
            except ValueError as err:
                raise RuntimeError from err
            except IOError as err:
                pass

        if state == fxe.FX_SUCCESS.value:
            print(f"{TARGETS[self.target]['name']} bootloader activated", flush=True)
        else:
            print(f"{TARGETS[self.target]['name']} bootloader not active", flush=True)
