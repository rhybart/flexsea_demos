from cleo import Application

from flexsea_demos.commands.current_control import CurrentControlCommand
from flexsea_demos.commands.impedance_control import ImpedanceControlCommand
from flexsea_demos.commands.open_control import OpenControlCommand
from flexsea_demos.commands.position_control import PositionControlCommand
from flexsea_demos.commands.read_only import ReadOnlyCommand
from flexsea_demos.commands.two_position_control import TwoPositionControlCommand
from flexsea_demos.utils import ApplicationConfig


# ============================================
#            FlexseaDemoApplication
# ============================================
class FlexseaDemoApplication(Application):
    """
    Defines the base `run_demos` command and adds each demo as a
    subcommand.
    """
    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__(config=ApplicationConfig())
        for command in self._get_commands():
            self.add(command())

    # -----
    # _get_commands
    # -----
    def _get_commands(self):
        commandList = [
            CurrentControlCommand,
            OpenControlCommand,
            PositionControlCommand,
            ReadOnlyCommand,
        ]
        return commandList
