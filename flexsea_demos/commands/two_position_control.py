from time import sleep
from time import time
from typing import Dict
from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu
import matplotlib
import matplotlib.pyplot as plt

from flexsea_demos.device import Device
from flexsea_demos.utils import init


# ============================================
#         TwoPositionControlCommand
# ============================================
class TwoPositionControlCommand(Command):
    """
    Runs the two position control demo.

    two_position_control
        {paramFile : Yaml file containing the parameters for the demo.}
    """
    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init()

        matplotlib.use("WebAgg")
        if fxu.is_pi():
            matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

        self.plot_data = {"times" : [], "requests" : [], "measurements" : []}

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the two position control demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        nLoops = int(params["run_time"] / 0.1)
        transition_steps = int(params["transition_time"] / 0.1)

        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            self._reset_plot()
            self._two_position_control(device, nLoops, transition_steps, params["gains"], params["delta"])
            device.motor(fxe.FX_VOLTAGE, 0)
            self._plot()
            device.close()

    # -----
    # _two_position_control
    # -----
    def _two_position_control(self, device, nLoops, transition_steps, gains, delta):
        data = device.read()
        initial_angle = data.mot_ang
        positions = [initial_angle, initial_angle + delta]
        current_pos = 0

        device.set_gains(50, 0, 0, 0, 0, 0)
        device.motor(fxe.FX_POSITION, initial_angle)
        start_time = time()

        for i in range(nLoops):
            sleep(0.1)
            data = device.read()
            fxu.clear_terminal()
            measured_pos = data.mot_ang
            print(f"Desired:              {positions[current_pos]}")
            print(f"Measured:             {measured_pos}")
            print(f"Difference:           {(measured_pos - positions[current_pos])}\n")
            device.print(data)

            if i % transition_steps == 0:
                current_pos = (current_pos + 1) % len(positions)
                device.motor(fxe.FX_POSITION, positions[current_pos])

            self.plot_data["times"].append(time() - start_time)
            self.plot_data["requests"].append(positions[current_pos])
            self.plot_data["measurements"].append(measured_pos)

    # -----
    # _plot
    # -----
    def _plot(self):
        plt.title("Two Position Control Demo")
        plt.plot(params["times"], params["requests"], color="b", label="Desired position")
        plt.plot(params["times"], params["measurements"], color="r", label="Measured position")
        plt.xlabel("Time (s)")
        plt.ylabel("Encoder position")
        plt.legend(loc="upper right")
        fxu.print_plot_exit()
        plt.show()

    # -----
    # _reset_plot
    # -----
    def _reset_plot(self):
        self.plot_data = {"times" : [], "requests" : [], "measurements" : []}
        plt.clf()

    # -----
    # _validate
    # -----
    def _validate(self, params):
        """
        The read_only demo requires at least one port, a baud rate,
        a run time, a delta, a transition time, and gains.

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
        required = {"ports" : List, "baud_rate" : int, "run_time" : int, "delta" : int, "transition_time" : float, "gains" : Dict}
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
