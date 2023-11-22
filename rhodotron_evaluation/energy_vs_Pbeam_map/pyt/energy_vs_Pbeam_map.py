import os, sys, json
import numpy as np

# ========================================================= #
# ===  energy_vs_Pbeam_map.py                           === #
# ========================================================= #

def energy_vs_Pbeam_map( paramFile=None ):

    # ------------------------------------------------- #
    # --- [1] argument                              --- #
    # ------------------------------------------------- #
    if ( paramFile is None ): sys.exit( "[energy_vs_Pbeam_map.py] paramFile == ???" )

    # ------------------------------------------------- #
    # --- [2] load parameters                       --- #
    # ------------------------------------------------- #
    with open( paramFile, "r" ) as f:
        params  = json.load( f )

    # ------------------------------------------------- #
    # --- [3] calculation                           --- #
    # ------------------------------------------------- #
    EandP = []
    for key,val in params.items():
        EandP += [ ( np.array( [ val["Energy"], val["Pbeam"] ] ) )[np.newaxis,:] ]
    EandP = np.concatenate( EandP, axis=0 )
    
    # ------------------------------------------------- #
    # --- [5] plot                                  --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    e_,p_                    = 0, 1
    pngFile                  = "png/energy_vs_Pbeam_map.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["FigSize"]        = (3.0,3.0)
    config["plt_position"]   = [ 0.20, 0.20, 0.90, 0.90 ]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [  0.0, +50.0 ]
    config["plt_yRange"]     = [  0.0, +600.0 ]
    config["xMajor_Nticks"]  =  6
    config["yMajor_Nticks"]  =  7
    config["xMinor_nticks"]  =  2
    config["yMinor_nticks"]  =  2
    config["plt_marker"]     = "D"
    config["plt_markersize"] = 8.0
    config["plt_linestyle"]  = "none"
    config["plt_linewidth"]  = 2.0
    config["xTitle"]         = "E (MeV)"
    config["yTitle"]         = "$P_{beam}$ (kW)"
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=EandP[ :,e_], yAxis=EandP[ :,p_], color="orange" )
    fig.add__plot( xAxis=EandP[-1,e_], yAxis=EandP[-1,p_], color="red" )
    fig.set__axis()
    fig.save__figure()


    
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    paramFile = "dat/parameters.json"
    energy_vs_Pbeam_map( paramFile=paramFile )
    
