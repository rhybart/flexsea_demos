import os

from cleo.config import ApplicationConfig as BaseApplicationConfig
from clikit.api.formatter import Style
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu
import yaml


# ============================================
#                    setup
# ============================================
def setup(cls, schema, paramFile):
    """
    Contains the boilerplate code for setting up a demo.

    Parameters
    ----------
    cls : cleo.Command
        The instance of the demo command to set up.

    schema : dict
        Names and types of the parameters required by the demo. Used to
        validate the data read from the parameter file.

    paramFile : str
        Name (and path) of the parameter file to read.
    """
    params = read_yaml(paramFile)
    params = validate(schema, params)
    assign_params(cls, params)
    setattr(cls, "fxs", flex.FlexSEA())


# ============================================
#                  validate
# ============================================
def validate(schema, data):
    """
    Makes sure that `data` has the keys contained in `schema` and that
    the values in `data` are of the type specified in `schema`.

    Parameters
    ----------
    schema : dict
        Keys are the names of the required parameters and the values
        are the types required for the corresponding parameter.

    data : dict
        The parameter/value pairs read in.

    Returns
    -------
    data : dict
        The validated data.
    """
    for requiredParam, requiredParamType in schema.items():
        try:
            assert requiredParam in data.keys()
        except AssertionError:
            raise AssertionError(f"'{requiredParam}' not found.")
        try:
            assert isinstance(data[requiredParam], requiredParamType)
        except AssertionError:
            msg = f"'{requiredParamType}' isn't the right type for '{requiredParam}'."
            raise AssertionError(msg)
    return data


# ============================================
#               assign_params
# ============================================
def assign_params(cls, params):
    """
    Sets the values of the parameters in `params` as attributes of the
    class `cls`.

    Parameters
    ----------
    cls : cle.Command
        The Command class for which we are setting attributes.

    params : dict
        Contains the attribute names and values to use as attributes.
    """
    for key, value in params.items():
        setattr(cls, key, value)


# ============================================
#                  read_yaml
# ============================================
def read_yaml(yamlFile):
    """
    Contains the boilerplate code for reading a yaml file.

    Parameters
    ----------
    yamlFile : str
        The name (including path) of the yaml file to read.

    Returns
    -------
    dict
        A dictionary containing the data read from the file.
    """
    yamlFile = sanitize_path(yamlFile)
    with open(yamlFile, "r") as inFile:
        data = yaml.safe_load(inFile)
    return data


# ============================================
#                sanitize_path
# ============================================
def sanitize_path(path):
    """
    Expands out environment variables, handles links, and makes sure
    that the file exists.

    Parameters
    ----------
    path : str
        The path to clean.

    Raises
    ------
    FileNotFoundError
        If the given path cannot be found.

    Returns
    -------
    str
        The expanded path.
    """
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Could not file parameter file: '{path}'")
    return path


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
