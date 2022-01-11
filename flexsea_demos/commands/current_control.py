from time import sleep
from typing import Dict
from typing import Int
from tying import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import init


# ============================================
#           CurrentControlCommand
# ============================================
class CurrentControlCommand(Command):
    """
    Runs the current control demo.

    current_control
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # handle
    # -----
    def handle(self):
        """
        Current control demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        nLoops = int(params["run_time"] / 0.1)
        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            device.set_gains(params["gains"])
            sleep(0.5)
            self._current_control(device, nLoops, params["hold_current"], params["ramp_down_steps"])

    # -----
    # _current_control
    # -----
    def _current_control(self, device, nLoops, hold_current, ramp_down_steps):
        for _ in range(nLoops):
            self._ramp(device, hold_current)
        for i in range(ramp_down_steps):
            current = hold_current * (ramp_down_steps - i) / ramp_down_steps
            self._ramp(device, current)
        device.motor(fxe.FX_NONE, 0)
        sleep(0.5)
        device.close()

    # -----
    # _ramp
    # -----
    def _ramp(self, device, current):
        """
        Adjusts the device's current and print's the actual measured
        value for comparison.
        """
        device.motor(fxe.FX_CURRENT, current)
        sleep(0.1)
        data = device.read()
        fxu.clear_terminal()
        print("Desired (mA):         ", current)
        print("Measured (mA):        ", data.mot_cur)
        print("Difference (mA):      ", (data.mot_cur - current), "\n")
        device.print(data)

    # -----
    # _validate
    # -----
    def _validate(self, params):
        """
        The current control demo requires at least one port, a baud rate,
        a run time, gains, a current to hold, and the number of ramp down steps.

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
        required = {"ports" : List, "baud_rate" : Int, "run_time" : Int, "gains" : Dict, "hold_current" : Int, "ramp_down_steps" : Int} 
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
