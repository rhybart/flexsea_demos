from time import sleep
from typing import List

from cleo import Command
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#          LeaderFollowerCommand
# ============================================
class LeaderFollower(Command):
    """
    Runs the leader follower demo.

    leader_follower
        {paramFile : Yaml file with demo parameters.}
    """
    # Schema of parameters required by the demo
    required = {
        "ports" : List,
        "baud_rate" : int,
        "run_time" : int
    }

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.run_time = 0
        self.nLoops = 0
        self.devices = []
        self.loop_delay = 0.05
        self.fxs = None

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the read_only demo.
        """
        setup(self, self.required, self.argument("paramFile"))
        self.nLoops = int(self.run_time / self.loop_delay)

        try:
            assert len(self.ports) == 2
        except AssertionError:
            raise AssertionError(f"Need two devices. Got: '{len(self.ports)}'")

        for i in range(2):
            self.devices.append(Device(self.fxs, self.ports[i], self.baud_rate)

        # Set first device to current controller with 0 current (0 torque)
        self.devices[0].set_gains(40, 400, 0, 0, 0, 128)
        self.devices[0].motor(fxe.FX_CURRENT, 0)

        # Set position controller for second device
        self.devices[1].set_gains(100, 1, 0, 0, 0, 0)
        self.devices[1].motor(fxe.FX_POSITION, initial_angle_1)

        self._leader_follower()

        print("Turning off position control...")
        for i in range(2):
            self.devices[i].set_gains(0, 0, 0, 0, 0, 0)
            self.devices[i].motor(fxe.FX_NONE, 0)
            sleep(0.5)
            self.devices[i].close()

    # -----
    # _leader_follower
    # -----
    def _leader_follower(self):
        leader_pos0 = self.devices[0].initial_position
        follower_pos0 = self.devices[1].initial_position

        leader_id = self.devices[0].dev_id
        follower_id = self.devices[1].dev_id

		for i in range(self.nLoops):
			sleep(self.loop_delay)
			fxu.clear_terminal()

			leader_data = self.devices[0].read()
			follower_data = self.devices[1].read()

			diff = leader_data.mot_ang - leader_pos0

			self.devices[1].motor(fxe.FX_POSITION, follower_pos0 + diff)

			print(f"Device {follower_id} following device {leader_id}\n")
            self.devices[1].print()
			print("")
			self.devices[0].print()
			fxu.print_loop_count(i, self.nLoops)
