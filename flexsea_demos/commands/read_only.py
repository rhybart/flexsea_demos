from time import sleep
from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import init


# ============================================
#              ReadOnlyCommand
# ============================================
class ReadOnlyCommand(Command):
    """
    Reads device data and prints it to the screen.

    read_only
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the read_only demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        nLoops = int(params["run_time"] / 0.1)
        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            self._read_only(device, nLoops)

    # -----
    # _read_only
    # -----
    def _read_only(self, device, nLoops):
        """
        Reads FlexSEA device and prints gathered data.

        Parameters
        ----------
        device : flexsea_demos.device.Device
            Object that manages the device information and state.

        nLoops : int
            Number of device reads to make. Derived from `params["run_time"]`.
        """
        for i in range(nLoops):
            fxu.print_loop_count(i, nLoops)
            sleep(0.1)
            fxu.clear_terminal()
            device.print()
        device.close()

    # -----
    # _validate
    # -----
    def _validate(self, params):
        """
        The read_only demo requires at least one port, a baud rate,
        and a run time.

        Parameters
        ----------
        params : dict
            The demo parameters read from the parameter file.

        Raises
        ------
        AssertionError
            If the name or type given for a parameter is invalid.

        Returns
        -------
        params : dict
            The validated parameters.
        """
        required = {"ports" : List, "baud_rate" : int, "run_time" : int}
        for requiredParam, requiredParamType in required.items():
            try:
                assert requiredParam in params.keys()
            except AssertionError:
                raise AssertionError(f"'{requiredParam}' not in parameter file.")
            try:
                assert isinstance(params[requiredParam], requiredParamType)
            except AssertionError:
                raise AssertionError(f"'{requiredParamType}' isn't the right type.")
        return params
