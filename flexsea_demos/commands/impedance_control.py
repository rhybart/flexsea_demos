from time import sleep
from time import time
from typing import Dict
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu
import matplotlib
import matplotlib.pyplot as plt

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#         ImpedanceControlCommand
# ============================================
class ImpedanceControlCommand(Command):
    """
    Runs the impedance control demo.

    impedance_control
        {paramFile : Yaml file with demo parameters.}
    """

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
        "run_time": int,
        "gains": Dict,
        "transition_time": float,
        "delta": int,
        "b_increments": int,
    }

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.run_time = 0
        self.gains = {}
        self.transition_time = 0.0
        self.delta = 0
        self.b_increments = 0
        self.nLoops = 0
        self.transition_steps = 0
        self.start_time = 0.0
        self.fxs = None
        self.plot_data = {"times": [], "requests": [], "measurements": []}

        matplotlib.use("WebAgg")
        if fxu.is_pi():
            matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

    # -----
    # handle
    # -----
    def handle(self):
        """
        Impedance control demo.
        """
        setup(self, self.required, self.argument("paramFile"))
        self.nLoops = int(self.run_time / 0.02)
        self.transition_steps = int(self.transition_time / 0.02)

        for port in self.ports:
            input("Press 'ENTER' to continue...")
            device = Device(self.fxs, port, self.baud_rate)
            self._reset_plot()

            self._impedance_control(device)

            device.motor(fxe.FX_VOLTAGE, 0)
            self._plot()
            device.close()

    # -----
    # _impedance_control
    # -----
    def _impedance_control(self, device):
        data = device.read()
        initial_angle = data.mot_ang
        device.motor(fxe.FX_IMPEDANCE, initial_angle)
        device.set_gains(self.gains)
        current_pos = 0
        positions = [initial_angle, initial_angle + self.delta]
        sleep(0.4)
        self.start_time = time()
        print("")

        for i in range(self.nLoops):
            data = device.read()
            measured_pos = data.mot_ang

            if i % self.transition_steps == 0:
                self.gains["B"] += self.b_increments
                device.set_gains(self.gains)
                self.delta = abs(positions[current_pos] - measured_pos)
                current_pos = (current_pos + 1) % 2
                device.motor(fxe.FX_IMPEDANCE, positions[current_pos])
            sleep(0.02)

            if i % 10 == 0:
                fxu.clear_terminal()
                print(f"Loop {i} of {self.nLoops}")
                print(f"Holding position: {positions[current_pos]}")
                print(self.gains)
                device.print(data)

            self.plot_data["measurements"].append(measured_pos)
            self.plot_data["times"].append(time() - self.start_time)
            self.plot_data["requests"].append(positions[current_pos])

    # -----
    # _plot
    # -----
    def _plot(self):
        title = "Impedance Control Demo"
        plt.plot(
            self.plot_data["times"],
            self.plot_data["requests"],
            color="b",
            label="Desired position",
        )
        plt.plot(
            self.plot_data["times"],
            self.plot_data["measurements"],
            color="r",
            label="Measured position",
        )
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
        self.plot_data = {"times": [], "requests": [], "measurements": []}
        plt.clf()
