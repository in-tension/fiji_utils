
""" int to use to set measurements to all"""

MEAS_ALL = 2092799
MEAS_GEO = 1076897
MEAS_INTENS = 2065502
MEAS_INTENS_XY = 2065534


POSS_PRJ_METHODS = ["avg", "min", "max", "sum", "sd", "median"]

GEO_HDINGS = [
    "Area", "Perim.", "X", "Y",
    "BX", "BY", "Width", "Height",
    "Major", "Minor", "Angle",
    "Feret", "FeretX", "FeretY", "FeretAngle", "MinFeret",
    "AR", "Round", "Solidity", "Circ."]

INTENS_HDINGS = [
    "%Area", "XM", "YM",
    "Mean", "StdDev", "Median", "Mode", "Min", "Max",
    "IntDen", "RawIntDen", "Skew"]
