import os, sys
import numpy as np
import solver__forcedCoolingAroundCylinder as fcc

# ========================================================= #
# ===  iterate__flow.py                                 === #
# ========================================================= #

def iterate__flow(  ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    iterFile = "dat/parameter_iter.conf"
    baseFile = "dat/parameter_base.conf"
    with open( baseFile, "r" ) as f:
        baseText = f.read()
    
    # ------------------------------------------------- #
    # --- [2] iterator                              --- #
    # ------------------------------------------------- #
    flowRate   = np.linspace( 10.0, 120.0, 12 )
    
    # ------------------------------------------------- #
    # --- [3] iterate solver                        --- #
    # ------------------------------------------------- #
    Data = []
    for ik,fr in enumerate( flowRate ):
        paramsContents = baseText.format( fr )
        with open( iterFile, "w" ) as f:
            f.write( paramsContents )
        ret = fcc.main( parameterFile=iterFile )
        Data += [ [ fr, ret[1] ] ]
    Data = np.array( Data )
        
    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/flow_scan.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )

    


# ========================================================= #
# ===  iterate__power.py                               === #
# ========================================================= #

def iterate__power(  ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    iterFile = "dat/parameter_iter.conf"
    baseFile = "dat/parameter_base.conf"
    with open( baseFile, "r" ) as f:
        baseText = f.read()
    
    # ------------------------------------------------- #
    # --- [2] iterator                              --- #
    # ------------------------------------------------- #
    beam_power = np.linspace( 5.0, 20.0, 16 )
    heat_load  = beam_power * 39.7 / 9.0
    
    # ------------------------------------------------- #
    # --- [3] iterate solver                        --- #
    # ------------------------------------------------- #
    Data = []
    for ik,hl in enumerate( heat_load ):
        paramsContents = baseText.format( hl )
        with open( iterFile, "w" ) as f:
            f.write( paramsContents )
        ret = fcc.main( parameterFile=iterFile )
        Data += [ [ beam_power[ik], hl, ret[1] ] ]
    Data = np.array( Data )
        
    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/power_scan.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )

    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    # iterate__power()
    iterate__flow()
