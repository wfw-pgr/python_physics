import numpy as np

# ========================================================= #
# ===  calculation of characteristics of helmholtz coil === #
# ========================================================= #

def output__helmhortz():

    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #

    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )

    # ------------------------------------------------- #
    # --- [2] print settings                        --- #
    # ------------------------------------------------- #
    print()
    print( "[output__helmhortz.py]  ---- parameters ---- " )
    print( "[output__helmhortz.py]  nCoil  :: {0:6d} (turn)".format( const["nCoil"]  ) )
    print( "[output__helmhortz.py]  ICoil  :: {0:.4f} (A)"  .format( const["ICoil"]  ) )
    print( "[output__helmhortz.py]  rCoil  :: {0:.4f} (m)"  .format( const["rCoil"] ) )
    print()
    
    # ------------------------------------------------- #
    # --- [3] calculation of output                 --- #
    # ------------------------------------------------- #
    coef = 0.8**1.5
    mu0  = 4.0 * np.pi * 1e-7
    Bval = coef * mu0 * const["nCoil"] * const["ICoil"] / const["rCoil"]

    # ------------------------------------------------- #
    # --- [4] display results                       --- #
    # ------------------------------------------------- #
    print()
    print( "[output__helmhortz.py]  ----   answer   ---- " )
    print( "[output__helmhortz.py]  B      :: {0:.6e} (T)".format( Bval ) )
    print()

    # ------------------------------------------------- #
    # --- [5] calculate characteristics             --- #
    # ------------------------------------------------- #

    #  -- [5-1] preparation                         --  #
    nI           = np.array( const["ICoil_variate"] ).shape[0]
    nR           = np.array( const["rCoil_variate"] ).shape[0]
    nN           = np.array( const["nCoil_variate"] ).shape[0]
    mT           = 1.e-3  #  mT :: (unit)

    #  -- [5-2] nCoil is given case                 --  #
    Data1        = np.zeros( (nI,nR,2) )
    for ik,rCoil in enumerate( const["rCoil_variate"] ):
        Data1[:,ik,0] = np.copy( np.array( const["ICoil_variate"] ) )
        Data1[:,ik,1] = coef * mu0 * const["nCoil"] * Data1[:,ik,0] / rCoil / mT

    #  -- [5-3] ICoil is given case                 --  #
    Data2        = np.zeros( (nR,nN,2) )
    for ik,nCoil in enumerate( const["nCoil_variate"] ):
        Data2[:,ik,0] = np.copy( np.array( const["rCoil_variate"] ) )
        Data2[:,ik,1] = coef * mu0 * nCoil * const["ICoil"] / Data2[:,ik,0] / mT

    #  -- [5-4] rCoil is given case                 --  #
    Data3        = np.zeros( (nI,nN,2) )
    for ik,nCoil in enumerate( const["nCoil_variate"] ):
        Data3[:,ik,0] = np.copy( np.array( const["ICoil_variate"] ) )
        Data3[:,ik,1] = coef * mu0 * nCoil * Data1[:,ik,0] / const["rCoil"] / mT

    # ------------------------------------------------- #
    # --- [6] display characteristics               --- #
    # ------------------------------------------------- #

    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf
    config   = lcf.load__config()
    config["FigSize"]        = (4,4)
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_linewidth"]  = 0.5
    config["plt_marker"]     = "x"
    config["plt_markersize"] = 4.0
    config["xMajor_Nticks"]  = 5
    config["yMajor_Nticks"]  = 5
    config["yTitle"]         = "B (mT)"

    label_r  = [ "r={0:.4} (m)".format( str( rCoil ) ) for rCoil in const["rCoil_variate"] ]
    label_n  = [ "n={0:3} ".format( str( int( nCoil ) ) ) for nCoil in const["nCoil_variate"] ]

    #  -- [6-1] display nCoil is fixed case         --  #
    pngFile          = "png/helmhortz_n_Fixed.png"
    config["xTitle"] = "I (A)"
    fig      = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( nR ):
        fig.add__plot( xAxis=Data1[:,ik,0], yAxis=Data1[:,ik,1], label=label_r[ik] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    #  -- [6-2] display ICoil is fixed case         --  #
    pngFile          = "png/helmhortz_I_Fixed.png"
    config["xTitle"] = "r (m)"
    fig      = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( nN ):
        fig.add__plot( xAxis=Data2[:,ik,0], yAxis=Data2[:,ik,1], label=label_n[ik] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    #  -- [6-3] display rCoil is fixed case         --  #
    pngFile          = "png/helmhortz_r_Fixed.png"
    config["xTitle"] = "I (A)"
    fig              = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( nN ):
        fig.add__plot( xAxis=Data3[:,ik,0], yAxis=Data3[:,ik,1], label=label_n[ik] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    return
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    output__helmhortz()
