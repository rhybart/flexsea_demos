from time import sleep
from typing import Int
from tying import List

from cleo import Command
from flexsea import flexsea as fxs
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import init


# ============================================
#              OpenControlCommand
# ============================================
class OpenControlCommand(Command):
    """
    Implements the open control demo.

    open_control
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the open_control demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        voltages = self._get_voltages(params["run_time"], params["n_cycles"], params["max_voltage"])
        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            self._open_control(device, params["n_cycles"], voltages)

    # -----
    # _get_voltages
    # -----
    def _get_voltages(self, runTime, nCycles, maxVoltage):
        """
        Generates the list of voltages to step through.

        Parameters
        ----------
        runTime : int
            The total time to run per device in seconds.

        nCycles : int
            The number of ramp-up/ramp-down cycles per device to fit in `runTime`.

        maxVoltage : int
            The peak voltage to ramp each device to.
        """
        cycle_time = runTime / float(nCycles)
        step_count = int((cycle_time / 2) / 0.1)
        return [-1 * maxVoltage * (s * 1.0 / step_count) for s in range(step_count)]

    # -----
    # _open_control
    # -----
    def _open_control(self, device, nCycles, voltages):
        print(f"Setting open control for port {port}...")
        device.motor(fxe.FX_VOLTAGE, 0)
        sleep(0.5)

        for rep in range(nCycles):
            # Ramp-up
            print(f"Ramping up motor voltage {rep}...\n")
            for voltage in voltages:
                self._ramp_device(device, voltage)
            # Ramp-down
            print(f"Ramping down motor voltage {rep}...\n")
            for voltage in voltages[-1::-1]:
                self._ramp_device(device, voltage)

        device.motor(fxe.FX_NONE, 0)
        sleep(0.1)
        device.close()

    # -----
    # _ramp_device
    # -----
    def _ramp_device(self, device, voltage):
        """
        Boilerplate for stepping through voltages.

        Parameters
        ----------
        device : flexsea_demos.device.Device
            Object that manages the device information and state.

        voltage_mv : float
            The voltage to set.
        """
        sleep(0.1)
        device.motor(fxe.FX_VOLTAGE, voltage_mv)
        fxu.clear_terminal()
        device.print()

    # -----
    # _validate
    # -----
    def _validate(self, params)
        """
        The read_only demo requires at least one port, a baud rate,
        a run time, the number of cycles per device, and the max voltage.

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
        required = {"ports" : List, "baud_rate" : Int, "run_time" : Int, "n_cycles" : Int, "max_voltage" : Int}
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
