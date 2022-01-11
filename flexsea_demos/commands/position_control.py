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
#          PositionControlCommand
# ============================================
class PositionControlCommand(Command):
    """
    Runs the position control demo.

    position_control
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # handle
    # -----
    def handle(self):
        """
        Position control demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        nLoops = int(params["run_time"] / 0.1)
        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            self._position_control(device, nLoops, params["gains"])

    # -----
    # _position_control
    # -----
    def _position_control(self, device, nLoops, gains):
        data = device.read()
        device.print(data)
        initial_angle = data.mot_ang
        device..set_gains(gains)
        device.motor(fxe.FX_POSITION, initial_angle)
        for i in range(nLoops):
            sleep(0.1)
            fxu.clear_terminal()
            data = device.read()
            current_angle = data.mot_ang
            print("Desired:              ", initial_angle)
            print("Measured:             ", current_angle)
            print(
                "Difference:           ",
                current_angle - initial_angle,
                "\n",
                flush=True,
            )
            device.print(data)
            fxu.print_loop_count(i, nLoops)
        device.motor(fxe.FX_NONE, 0)
        sleep(0.5)
        device.close()

    # -----
    # _validate
    # -----
    def _validate(self, params):
        """
        The position control demo requires at least one port, a baud rate,
        a run time, and gains.

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
        required = {"ports" : List, "baud_rate" : Int, "run_time" : int, "gains" : Dict}
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
