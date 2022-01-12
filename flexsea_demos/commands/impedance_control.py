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
#         ImpedanceControlCommand
# ============================================
class ImpedanceControlCommand(Command):
    """
    Runs the impedance control demo.

    impedance_control
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()

        matplotlib.use("WebAgg")
        if fxu.is_pi():
            matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

        self.plot_data = {"times" : [], "requests" : [], "measurements" : []}

    # -----
    # handle
    # -----
    def handle(self):
        """
        Impedance control demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        nLoops = int(params["run_time"] / 0.02)
        transition_steps = int(params["transition_time"] / 0.02)

        for port in params["ports"]:
            input("Press 'ENTER' to continue...")
            device = Device(fxs, port, params["baud_rate"])
            self._reset_plot()

            self._impedance_control(device, nLoops, transition_steps, params["gains"], params["delta"], params["b_increments"])

            device.motor(fxe.FX_VOLTAGE, 0)
            self._plot()
            device.close()

    # -----
    # _impedance_control
    # -----
    def _impedance_control(self, device, nLoops, transition_steps, gains, delta, b_increments):
        data = device.read()
        initial_angle = data.mot_ang
        device.motor(fxe.FX_IMPEDANCE, initial_angle)
        device.set_gains(gains)
        current_pos = 0
        positions = [initial_angle, initial_angle + delta]
        sleep(0.4)
        start_time = time()
        print("")

        for i in range(nLoops):
            data = device.read()
            measured_pos = data.mot_ang

            if i % transition_steps == 0:
                gains["B"] += b_increments
                device.set_gains(gains)
                delta = abs(positions[current_pos] - measured_pos)
                current_pos = (current_pos + 1) % 2
                device.motor(fxe.FX_IMPEDANCE, positions[current_pos])
            sleep(0.02)

            if i % 10 == 0:
                fxu.clear_terminal()
                print(f"Loop {i} of {num_timesteps}")
                print(f"Holding position: {positions[current_pos]}")
                print(gains)
                device.print(data)

            self.plot_data["measurements"].append(measured_pos)
            self.plot_data["times"].append(time() - start_time)
            self.plot_data["requests"].append(positions[current_pos])

    # -----
    # _plot
    # -----
    def _plot(self):
        title = "Impedance Control Demo"
        plt.plot(self.plot_data["times"], self.plot_data["requests"], color="b", label="Desired position")
        plt.plot(self.plot_data["times"], self.plot_data["measurements"], color="r", label="Measured position")
        plt.xlabel("Time (s)")
        plt.ylabel("Encoder position")
        plt.title(title)
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
        The impedance control demo requires at least one port, a baud rate,
        a run time, gains, a transition time, a delta, and a b gain increment.

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
        required = {"ports" : List, "baud_rate" : int, "run_time" : int, "gains" : Dict, "transition_time" : float, "delta" : int, "b_increments" : int}
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
