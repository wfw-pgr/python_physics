import numpy as np

# ========================================================= #
# ===  formula__forcedCoolingAroundCylinder.py          === #
# ========================================================= #

def formula__forcedCoolingAroundCylinder():

    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [2] calculate Reynolds Number             --- #
    # ------------------------------------------------- #
    const["pipe.area"]       = const["pipe.diameter"]**2 * np.pi / 4
    const["pipe.flow.m3_s"]  = const["pipe.flow.L_min"] * 1e-3 / 60.0
    const["fluid.velocity"]  = const["pipe.flow.m3_s"] / const["pipe.area"]
    const["fluid.Re"]        = const["fluid.velocity"] * const["target.diameter"] \
        / const["fluid.viscosity"]

    # ------------------------------------------------- #
    # --- [3] Nusselt Number & heat transfer        --- #
    # ------------------------------------------------- #
    const["fluid.Nu"]        = const["coeff.c"] * const["fluid.Re"]**const["coeff.m"] \
        * const["fluid.prandtl"] ** ( 1./3. )
    const["heat_transfer"]   = const["fluid.Nu"] * const["fluid.thermalConductivity"] \
        / const["target.diameter"]

    # ------------------------------------------------- #
    # --- [4] tempature estimation                  --- #
    # ------------------------------------------------- #
    const["target.area"]     = 2.0*( np.pi / 4 * const["target.diameter"]**2 ) \
        + np.pi * const["target.diameter"] * const["target.length"]
    const["target.dT"]       = const["target.heatload"] \
        / ( const["heat_transfer"] * const["target.area"] )
    const["target.T"]        = const["fluid.temperature_infty"] + const["target.dT"]

    # ------------------------------------------------- #
    # --- [5] display results                       --- #
    # ------------------------------------------------- #
    print( "\n" + "-" * 70 )
    print( "{0:>30} :: {1:>30}".format( "key", "value" ) )
    print( "-" * 70 )
    for key,value in const.items():
        print( "{0:>30} :: {1:>30}".format( key, value ) )
    print( "-" * 70 + "\n" )
        
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    formula__forcedCoolingAroundCylinder()
