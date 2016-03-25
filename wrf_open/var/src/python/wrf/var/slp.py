from .extension import computeslp, computetk
from .constants import Constants
from .destag import destagger
from .decorators import convert_units, copy_and_set_metadata
from .util import extract_vars

__all__ = ["get_slp"]

@copy_and_set_metadata(copy_varname="T", name="slp",
                       remove_dims=("bottom_top",), 
                       description="sea level pressure")
@convert_units("pressure", "hpa")
def get_slp(wrfnc, timeidx=0, units="hpa", 
            method="cat", squeeze=True, cache=None):
    varnames=("T", "P", "PB", "QVAPOR", "PH", "PHB")
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache)

    t = ncvars["T"]
    p = ncvars["P"]
    pb = ncvars["PB"]
    qvapor = ncvars["QVAPOR"]
    ph = ncvars["PH"]
    phb = ncvars["PHB"]
    
    full_t = t + Constants.T_BASE
    full_p = p + pb
    qvapor[qvapor < 0] = 0.
    full_ph = (ph + phb) / Constants.G
    
    destag_ph = destagger(full_ph, -3)
    
    tk = computetk(full_p, full_t)
    slp = computeslp(destag_ph, tk, full_p, qvapor)
    
    return slp

