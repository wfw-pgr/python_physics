import numpy as np
import nkUtilities.load__pointFile as lpf
        
# ========================================================= #
# ===  prepare__constants                             === #
# ========================================================= #
def prepare__constants( inpFile="dat/parameter.conf" ):

    # ------------------------------------------------- #
    # --- [1] load parameter.conf                   --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    params  = lcn.load__constants( inpFile=inpFile )

    # ------------------------------------------------- #
    # --- [2] parameter check                       --- #
    # ------------------------------------------------- #
    keys    = ["pipe.diameter", "pipe.flow.L_min", \
               "target.diameter", "target.length", "fluid.prandtl" , \
               "fluid.thermalConductivity", "target.heatload", \
               "fluid.temperature_infty", "target.T" ]
    for key in keys:
        if ( not( key in params ) ):
            print( "[nonLinear_formula__forcedCoolingAroundCylinder.py] key = {} cannot be found... [ERROR]".format( key ) )

    # ------------------------------------------------- #
    # --- [3] calculate dependent variables         --- #
    # ------------------------------------------------- #
    params["pipe.area"]       = params["pipe.diameter"]**2 * np.pi / 4
    params["pipe.flow.m3_s"]  = params["pipe.flow.L_min"] * 1e-3 / 60.0
    params["fluid.velocity"]  = params["pipe.flow.m3_s"] / params["pipe.area"]
    params["target.area"]     = 2.0*( np.pi / 4 * params["target.diameter"]**2 ) \
        + np.pi * params["target.diameter"] * params["target.length"]
    return( params )


# ========================================================= #
# ===  update__physicalProperty                         === #
# ========================================================= #

def update__physicalProperty( temperature=None, conductivity_fit=None, viscosity_fit=None, \
                              conductivityFile="dat/thermalConductivity.dat", viscosityFile="dat/viscosity.dat" ):

    T_, c_, v_ = 0, 1, 1
    
    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( temperature is None ):
        print( "temperature == ???" )
        sys.exit()

    # ------------------------------------------------- #
    # --- [2] update thermal conductivity           --- #
    # ------------------------------------------------- #
    if ( conductivity_fit is None ):
        conductivity     = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
        conductivity_fit = sp.interpolate.interp1d( conductivity[:,T_], conductivity[:,c_], kind="linear" )
    else:
        tc               = conductivity_fit( temperature )
    
    # ------------------------------------------------- #
    # --- [3] update viscosity                      --- #
    # ------------------------------------------------- #
    if ( viscosity_fit    is None ):
        viscosity        = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
        viscosity_fit    = sp.interpolate.interp1d( conductivity[:,T_], conductivity[:,c_], kind="linear" )
    else:
        nu               = viscosity_fit   ( temperature )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( (temperature,tc,nu) )

    
# ========================================================= #
# ===  linear__forcedCoolingAroundCylinder.py           === #
# ========================================================= #

def linear__forcedCoolingAroundCylinder( params=None ):

    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( params is None ): sys.exit( "[nonLinear_formula__forcedCoolingAroundCylinder.py] params == ???" )

    # ------------------------------------------------- #
    # --- [2] update variables                      --- #
    # ------------------------------------------------- #
    params["target.Told"]   = params["target.T"]
    params["fluid.Re"]      = params["fluid.velocity"] * params["target.diameter"] / params["fluid.viscosity"]
    params["fluid.Nu"]      = params["coef.c"] * params["fluid.Re"]**params["coef.m"] * params["fluid.prandtl"] ** ( 1./3. )
    params["heat_transfer"] = params["fluid.Nu"] * params["fluid.thermalConductivity"] / params["target.diameter"]
    params["target.dT"]     = params["target.heatload"] / ( params["heat_transfer"] * params["target.area"] )
    params["target.T"]      = params["fluid.temperature_infty"] + params["target.dT"]
    return( params )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile = "dat/parameter.conf"
    
    params = prepare__constants( inpFile=inpFile )
    linear__forcedCoolingAroundCylinder( params=params )
    print( params )
