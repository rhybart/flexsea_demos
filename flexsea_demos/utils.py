import os

from cleo.config import ApplicationConfig as BaseApplicationConfig
from clikit.api.formatter import Style
import matplotlib
import yaml


# ============================================
#                     init
# ============================================
def init(paramFile, validate_func):
    """
    Contains the boilerplate code for reading and validating the
    parameter file.

    Parameters
    ----------
    paramFile : str
        The name (including path) of the demo's parameter file.

    validate_func : Callable
        The demo's `_validate` function.

    Returns
    -------
    dict
        A dictionary containing the validated parameters to use in the
        demo.
    """
    matplotlib.use("WebAgg")
    if fxu.is_pi():
        matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})
    paramFile = sanitize_path(paramFile)
    with open(paramFile, "r") as inFile:
        params = yaml.safe_load(inFile)
    return validate_func(params)


# ============================================
#                sanitize_path
# ============================================
def sanitize_path(paramFile):
    """
    Expands out environment variables, handles links, and makes sure
    that the file exists.

    Parameters
    ----------
    paramFile : str
        The parameter file name for the demo (including path).

    Raises
    ------
    FileNotFoundError
        If the given file cannot be found.

    Returns
    -------
    str
        The expanded and validated file name and path.
    """
    paramFile = os.path.expandvars(paramFile)
    paramFile = os.path.expanduser(paramFile)
    paramFile = os.path.abspath(paramFile)
    if not os.path.isfile(paramFile):
        raise FileNotFoundError(f"Could not file parameter file: '{paramFile}'")
    return paramFile


# ============================================
#              ApplicationConfig
# ============================================
class ApplicationConfig(BaseApplicationConfig):
    def configure(self):
        super().configure()
        self.add_style(Style("info").fg("cyan"))
        self.add_style(Style("error").fg("red").bold())
        self.add_style(Style("warning").fg("yellow").bold())
        self.add_style(Style("success").fg("green"))
