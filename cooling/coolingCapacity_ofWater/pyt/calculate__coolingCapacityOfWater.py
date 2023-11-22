import os, sys, json
import numpy as np

# ========================================================= #
# ===  calculate__coolingCapacityOfWater.py             === #
# ========================================================= #

def calculate__coolingCapacityOfWater( paramFile=None ):

    # ------------------------------------------------- #
    # --- [1] argument                              --- #
    # ------------------------------------------------- #
    if ( paramFile is None ): sys.exit( "[calculate__coolingCapacityOfWater.py] paramFile == ???" )

    # ------------------------------------------------- #
    # --- [2] load parameters                       --- #
    # ------------------------------------------------- #
    with open( paramFile, "r" ) as f:
        params  = json.load( f )

    # ------------------------------------------------- #
    # --- [3] calculation                           --- #
    # ------------------------------------------------- #
    c     = params["specific_heat"]        # KJ/kgK
    rho   = params["density"]              # kg/m3
    u     = params["flow_speed"]           # m/s
    ap    = params["pipe_length_a"]        # m
    bp    = params["pipe_length_b"]        # m
    npipe = params["number_of_pipes"]      # -
    delT  = params["temperature_increase"] # K
    A     = ap * bp * npipe                # m2
    vol   = A * u                          # m3/s
    Qh    = c * rho * vol * delT           # KJ/s
    Qf    = vol * 1.0e3 * 60.0             # L/min
    u_var = np.linspace( 0.0, 4.0, 5 )
    Q_var = c * rho * A * u_var * delT

    # ------------------------------------------------- #
    # --- [4] display representative value          --- #
    # ------------------------------------------------- #
    print( "Qh :: {}".format( Qh ) )
    print( "Qf :: {}".format( Qf ) )
    
    # ------------------------------------------------- #
    # --- [5] plot                                  --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "png/calculate__coolingCapacityOfWater.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["FigSize"]        = (3.0,3.0)
    config["plt_position"]   = [ 0.20, 0.20, 0.90, 0.90 ]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [  0.0, +4.0 ]
    config["plt_yRange"]     = [  0.0, +150 ]
    config["xMajor_Nticks"]  =  5
    config["yMajor_Nticks"]  =  6
    config["xMinor_nticks"]  =  5
    config["yMinor_nticks"]  =  5
    config["plt_marker"]     = "o"
    config["plt_markersize"] = 6.0
    config["plt_linestyle"]  = "-"
    config["plt_linewidth"]  = 2.0
    config["xTitle"]         = "u (m/s)"
    config["yTitle"]         = "P (kW)"
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=u_var, yAxis=Q_var )
    fig.set__axis()
    fig.save__figure()


    
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    paramFile = "dat/parameters.json"
    calculate__coolingCapacityOfWater( paramFile=paramFile )
    
