import numpy as np


# ========================================================= #
# ===  child_langmuir_law                               === #
# ========================================================= #


def child_langmuir_law():


    Va_min  = 0.0
    Va_max  = 500e3
    nVa     = 101

    de_min  =  10.0e-3
    de_max  =  50.0e-3
    nde     =  5

    pngFile = "png/child_langmuir.png"
    
    # ------------------------------------------------- #
    # --- [1] calculation                           --- #
    # ------------------------------------------------- #

    epsilon = 8.854187e-12
    qe      = 1.602176e-19
    me      = 9.109383e-31
    Va      = np.linspace( Va_min, Va_max, nVa )
    de      = np.linspace( de_min, de_max, nde )
    Jcl     = np.zeros( ( nVa, nde ) )
    
    for ide in range( nde ):
        Jcl[:,ide] = 4.0 * epsilon / 9.0 * np.sqrt( 2.0 * qe / me ) * Va**(3.0/2.0) / de[ide]**2

    Amm2_unit = 1.e-6
    kV_unit   = 1.e-3
    Jcl_      = Jcl * Amm2_unit
    Va_       = Va * kV_unit
    # ------------------------------------------------- #
    # --- [2] plot characteristic                   --- #
    # ------------------------------------------------- #

    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf

    config = lcf.load__config()
    config["xTitle"] = "V (kV)"
    config["yTitle"] = "J (A/mm^2)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [0.0,500.0]
    config["plt_yRange"]     = [0.0,2.0]
    config["plt_linewidth"]  = 2.0
    config["xMajor_Nticks"]  = 6
    config["yMajor_Nticks"]  = 6


    
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    for ide in range( nde ):
        hlabel = "d={0:.5}".format( de[ide] )
        fig.add__plot( xAxis=Va_, yAxis=Jcl_[:,ide], label=hlabel )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    child_langmuir_law()



