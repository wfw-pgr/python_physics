import os, sys
import numpy as np
import scipy as sp

# ========================================================= #
# ===  prepare__parameters                              === #
# ========================================================= #
def prepare__parameters( inpFile="dat/parameter.conf" ):

    x_, y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] load parameter.conf                   --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    params  = lcn.load__constants( inpFile=inpFile )

    # ------------------------------------------------- #
    # --- [2] calculate dependent variables         --- #
    # ------------------------------------------------- #
    params["pipe.area"]       = params["pipe.diameter"]**2 * np.pi / 4
    params["pipe.flow.m3_s"]  = params["pipe.flow.L_min"] * 1e-3 / 60.0
    params["fluid.velocity"]  = params["pipe.flow.m3_s"] / params["pipe.area"]
    params["target.area"]     = 2.0*( np.pi / 4 * params["target.diameter"]**2 ) + np.pi * params["target.diameter"] * params["target.length"]

    # ------------------------------------------------- #
    # --- [3] load physical property                --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    tCondData = lpf.load__pointFile(inpFile=params["fluid.tConductivityFile"] )
    viscoData = lpf.load__pointFile(inpFile=params["fluid.viscosityFile"]     )
    params["tConductivity_fit"] = sp.interpolate.interp1d( tCondData[:,x_], tCondData[:,y_], \
                                                           fill_value="extrapolate"  )
    params["viscosity_fit"]     = sp.interpolate.interp1d( viscoData[:,x_], viscoData[:,y_], \
                                                           fill_value="extrapolate"  )

    # ------------------------------------------------- #
    # --- [4] load HilpertModel Coefficient         --- #
    # ------------------------------------------------- #
    coeffData = lpf.load__pointFile(inpFile=params["fluid.HilpertCoeffFile"]  )
    min_, max_, c_, m_ = 0, 1, 2, 3
    eps                    = 1.e-8
    coeffData[:,max_]    = coeffData[:,max_] - eps
    xD    = np.concatenate( [ coeffData[:,min_][None,:], coeffData[:,max_][None,:] ], axis=0 )
    cD    = np.concatenate( [ coeffData[:,c_  ][None,:], coeffData[:,c_  ][None,:] ], axis=0 )
    mD    = np.concatenate( [ coeffData[:,m_  ][None,:], coeffData[:,m_  ][None,:] ], axis=0 )
    xD    = np.reshape( xD, (-1,) )
    cD    = np.reshape( cD, (-1,) )
    mD    = np.reshape( mD, (-1,) )
    params["HilpertCoeff_c_fit"]  = sp.interpolate.interp1d( xD, cD, fill_value="extrapolate" )
    params["HilpertCoeff_m_fit"]  = sp.interpolate.interp1d( xD, mD, fill_value="extrapolate" )
    
    return( params )


# ========================================================= #
# ===  display__variables                               === #
# ========================================================= #

def display__variables( params=None, skip_keys=None ):

    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( params is None ): sys.exit( "[display__variables.py] params == ???" )
    if ( skip_keys is None ):
        skip_keys = [ "control.iterMax", "control.maxResidual", "control.verbose", \
                      "tConductivity_fit", "viscosity_fit", \
                      "HilpertCoeff_c_fit", "HilpertCoeff_m_fit" ]
    keys = list( set( params.keys() ) - set( skip_keys ) )
        
    # ------------------------------------------------- #
    # --- [2] display                               --- #
    # ------------------------------------------------- #
    print( "\n" + "-"*70 )
    print( " {0:>30} :: {1:>30} ".format( "key", "value" ) )
    print( "-"*70 )
    for key in keys:
        print( " {0:>30} :: {1:>30} ".format( key, params[key] ) )
    print( "-"*70 + "\n" )
    return()
    

# ========================================================= #
# ===  main.py                                          === #
# ========================================================= #

def main( parameterFile=None ):
    
    # ------------------------------------------------- #
    # --- [1] arguments check & load parameters     --- #
    # ------------------------------------------------- #
    if ( parameterFile is None ): parameterFile="dat/parameter.conf"
    params    = prepare__parameters( inpFile=parameterFile )
    print( "\n" + "="*90 )
    print( "[solver__forcedCoolingAroundCylinder.py] Begin Main Loop" )
    print( "="*90 + "\n" )

    # ------------------------------------------------- #
    # --- [2] Main Loop                             --- #
    # ------------------------------------------------- #
    for ik in range( params["control.iterMax"] ):

        # ------------------------------------------------- #
        # --- [4-1] update physical property            --- #
        # ------------------------------------------------- #
        params["fluid.thermalConductivity"] = params["tConductivity_fit"]( params["target.T"] )
        params["fluid.viscosity"]           = params["viscosity_fit"]    ( params["target.T"] )
        
        # ------------------------------------------------- #
        # --- [4-2] update cooled temperature           --- #
        # ------------------------------------------------- #
        params["target.Told"]   = params["target.T"]
        params["fluid.Re"]      = params["fluid.velocity"] * params["target.diameter"] / params["fluid.viscosity"]
        params["coeff.c"]       = params["HilpertCoeff_c_fit"]( params["fluid.Re"] )
        params["coeff.m"]       = params["HilpertCoeff_m_fit"]( params["fluid.Re"] )
        params["fluid.Nu"]      = params["coeff.c"] * params["fluid.Re"]**params["coeff.m"] * params["fluid.prandtl"] ** ( 1./3. )
        params["heat_transfer"] = params["fluid.Nu"] * params["fluid.thermalConductivity"] / params["target.diameter"]
        params["target.dT"]     = params["target.heatload"] / ( params["heat_transfer"] * params["target.area"] )
        params["target.T"]      = params["fluid.temperature_infty"] + params["target.dT"]
        params["target.T"]      = params["target.Told"] + params["control.relaxation"] * ( params["target.T"] - params["target.Told"] )

        # ------------------------------------------------- #
        # --- [4-3] check convergence                   --- #
        # ------------------------------------------------- #
        residual = np.abs( params["target.T"] - params["target.Told"] ) / ( params["target.Told"] )
        if ( residual < params["control.maxResidual"] ):
            converged = True
            print( "\n" + "="*90 )
            print( " Reach convergence.   at #. of iteration :: {}".format( ik ) )
            print( "="*90 + "\n" )
            print( " ( iteration, temperature, residual ) == ( {0:8}, {1:10.4f}, {2:10.4e} )".format( ik, params["target.T"], residual ) )
            display__variables( params=params )
            print( "\n" + "="*90 + "\n" )
            break

        # ------------------------------------------------- #
        # --- [4-4] display variables                   --- #
        # ------------------------------------------------- #
        if ( params["control.verbose"] ):
            print( "\n" + "-"*80 )
            print( " iteration :: {}".format( ik ) )
            print( "-"*80 + "\n" )
            print( " ( iteration, temperature, residual ) == ( {0:8}, {1:10.4f}, {2:10.4f} )".format( ik, params["target.T"], residual ) )
            display__variables( params=params )
            print( "\n" + "-"*80 + "\n" )
        else:
            print( " ( iteration, temperature, residual ) == ( {0:8}, {1:10.4f}, {2:10.4f} )".format( ik, params["target.T"], residual ) )
            
    if ( not( converged ) ):
        print( "\n" + "[solver__forcedCoolingAroundCylinder.py] does not converged... [CAUTION] " + "\n" )
            

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    parameterFile = "dat/parameter.conf"
    main( parameterFile=parameterFile )
