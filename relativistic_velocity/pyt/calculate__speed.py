import numpy as np

# ========================================================= #
# ===  calculate__speed.py                              === #
# ========================================================= #

def calculate__speed():

    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    cnsFile = "dat/parameter.conf"
    import nkUtilities.load__constants as lcn
    const   = lcn.load__constants( inpFile=cnsFile )

    # ------------------------------------------------- #
    # --- [2] make energy axis                      --- #
    # ------------------------------------------------- #
    energy  = np.array( [], )
    if ( const["log_energy"] ):
        for ik in range( const["energy_digit"] ):
            edigit  = 10**ik
            evalu   = np.linspace( 1.0, 9.0, 9 )
            henergy = evalu * edigit
            energy  = np.concatenate( [energy,henergy] )
    else:
        energy  = np.linspace( const["EMin"], const["EMax"], const["nE"],  )

    # ------------------------------------------------- #
    # --- [3] calculate beta & gamma                --- #
    # ------------------------------------------------- #
    # -- K = mc**2 / sqrt( 1 - beta**2 ) - mc**2 -- #
    # -- beta  -- #
    beta    = np.sqrt( 1.0 - ( 1.0 / ( 1.0 + ( const["qe"]*energy  ) / ( const["mp"]*const["cv"]**2 )  )**2 ) )
    # -- gamma -- #
    gamma   = 1.0 / np.sqrt( 1.0 - beta**2 )
    speed   = beta * const["cv"]
    
    # ------------------------------------------------- #
    # --- [4] save in file                          --- #
    # ------------------------------------------------- #
    e_,b_,g_,s_ = 0, 1, 2, 3
    Data        = np.zeros( (energy.shape[0],4) )
    Data[:,e_]  = energy
    Data[:,b_]  = beta
    Data[:,g_]  = gamma
    Data[:,s_]  = speed
    outFile     = "dat/relativistic_velocity.dat"
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=Data )

    # ------------------------------------------------- #
    # --- [5] plot figure                           --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf
    config                   = lcf.load__config()
    config["plt_xlog"]       = True
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["grid_sw"]        = True
    config["grid_minor_sw"]  = True
    config["xMinor_sw"]      = True
    config["xMajor_Nticks"]  = 6
    config["xMinor_Nticks"]  = 3
    config["yMinor_Nticks"]  = 3

    # -- beta     -- #
    config["plt_ylog"]       = False
    config["plt_xRange"]     = [1.0,1.0e10]
    config["plt_yRange"]     = [0.0,1.0   ]
    config["yMajor_Nticks"]  = 6
    pngFile = "png/relativistic_beta.png"
    print( config["xMinor_Nticks"] )
    fig     = pl1.plot1D( xAxis=Data[:,e_], yAxis=Data[:,b_], config=config, pngFile=pngFile )
    # -- gamma    -- #
    config["plt_ylog"]       = True
    config["plt_xRange"]     = [1.0,1.0e10]
    config["plt_yRange"]     = [1.0,2.0e5 ]
    config["yMajor_Nticks"]  = 6
    pngFile = "png/relativistic_gamma.png"
    fig     = pl1.plot1D( xAxis=Data[:,e_], yAxis=Data[:,g_], config=config, pngFile=pngFile )
    # -- velocity -- #
    config["plt_ylog"]       = False
    config["plt_xRange"]     = [1.0,1.0e10]
    config["plt_yRange"]     = [0.0,3.0e8 ]
    config["yMajor_Nticks"]  = 4
    pngFile = "png/relativistic_velocity.png"
    fig     = pl1.plot1D( xAxis=Data[:,e_], yAxis=Data[:,s_], config=config, pngFile=pngFile )


    
    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    calculate__speed()
