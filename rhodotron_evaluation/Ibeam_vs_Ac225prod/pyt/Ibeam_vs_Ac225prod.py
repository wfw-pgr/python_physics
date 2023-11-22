import os, sys, json
import numpy as np

# ========================================================= #
# ===  Ibeam_vs_Ac225prod.py                            === #
# ========================================================= #

def Ibeam_vs_Ac225prod( paramFile=None ):

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
    # -- coef :: Bq(Ac)/(Bq(Ra).uA) -- #
    linacD      = params["Linac"]
    RhodoD      = params["Rhodotron"]
    duration_L  = linacD["duration_day"] * 24.0             # [h]
    duration_R  = linacD["duration_day"] * 24.0             # [h]
    current_L   = linacD["power"] / linacD["Energy"] * 1e6  # [uA]
    current_R   = RhodoD["power"] / RhodoD["Energy"] * 1e6  # [uA]
    print( current_L, current_R )
    
    # -- coef ::  -- #
    coef_L      = linacD["efficiency"] * linacD["Ra-226"] * duration_L # [ Bq(Ac)/(Bq(Ra).uA) ]
    coef_R      = RhodoD["efficiency"] * RhodoD["Ra-226"] * duration_R # [ Bq(Ac)/(Bq(Ra).uA) ]
    AcProd_L    = coef_L * current_L * 1.0e-9  # [GBq(Ac)]
    AcProd_R    = coef_R * current_R * 1.0e-9  # [GBq(Ac)]
    AcProd_C    = AcProd_L * 11.0/20.0         # [GBq(Ac)]   , Current Status
    
    # -- estimation line -- #
    powerAxis   = np.linspace( *( params["powerAxisRange"] ) )
    IbeamAxis_L = powerAxis / linacD["Energy"] * 1e6 # [uA]
    IbeamAxis_R = powerAxis / RhodoD["Energy"] * 1e6 # [uA]
    EstLine_L   = coef_L * IbeamAxis_L * 1.0e-9      # [GBq(Ac)]
    EstLine_R   = coef_R * IbeamAxis_R * 1.0e-9      # [GBq(Ac)]
    EstLine_C   = EstLine_L * 11.0/20.0              # [GBq(Ac)]
    powerAxis_  = powerAxis * 1.0e-3
    print( AcProd_L, AcProd_R, AcProd_C )
    
    # ------------------------------------------------- #
    # --- [4] plot                                  --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    e_,p_                    = 0, 1
    pngFile                  = "png/Ibeam_vs_Ac225prod.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["FigSize"]        = (4.0,4.0)
    config["plt_position"]   = [ 0.18, 0.18, 0.94, 0.94 ]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [  0.0, +150.0 ]
    config["plt_yRange"]     = [  0.0,  +40.0 ]
    config["xMajor_Nticks"]  =  4
    config["yMajor_Nticks"]  =  5
    config["xMinor_nticks"]  =  5
    config["yMinor_nticks"]  =  2
    config["plt_marker"]     = "none"
    config["plt_markersize"] = 8.0
    config["plt_linestyle"]  = "none"
    config["plt_linewidth"]  = 2.0
    config["xTitle"]         = "$P_{beam}$ (kW)"
    config["yTitle"]         = "$q_{Ac}$ (GBq)"
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=powerAxis_, yAxis=EstLine_L, color="C1", \
                   linestyle="--", linewidth=1.2 )
    fig.add__plot( xAxis=powerAxis_, yAxis=EstLine_C, color="C0", \
                   linestyle="--", linewidth=1.2 )
    fig.add__plot( xAxis=powerAxis_, yAxis=EstLine_R, color="C2", \
                   linestyle="--", linewidth=1.2 )
    fig.add__plot( xAxis=linacD["power"]*1e-3, yAxis=AcProd_L, color="C1",\
                   linestyle="none", marker="*", markersize=16.0 )
    fig.add__plot( xAxis=linacD["power"]*1e-3, yAxis=AcProd_C, color="C0",\
                   linestyle="none", marker="*", markersize=12.0 )
    fig.add__plot( xAxis=RhodoD["power"]*1e-3, yAxis=AcProd_R, color="C2",\
                   linestyle="none", marker="D" )
    fig.set__axis()
    fig.save__figure()


    
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    paramFile = "dat/parameters.json"
    Ibeam_vs_Ac225prod( paramFile=paramFile )
    
