import os, sys
import numpy as np


# ========================================================= #
# ===  fit__magneticMoment.py                           === #
# ========================================================= #

def fit__magneticMoment():

    pngFile = "png/bfield_fited.png"
    inpFile = "dat/magneticMoment.dat"

    # ------------------------------------------------- #
    # --- [1] load data to be fitted                --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    zval    = Data[:,0]
    bval    = Data[:,1]
    
    # ------------------------------------------------- #
    # --- [2] fit__magneticMoment                   --- #
    # ------------------------------------------------- #
    import scipy.optimize as opt
    popt, pcov = opt.curve_fit( eq__magneticMoment, zval, bval )
    zfit = np.linspace( np.min(zval), np.max(zval), 101 )
    bfit = eq__magneticMoment( zfit, popt[0], popt[1] )
    print()
    print( "[fit__magneticMoment.py] fitted value.... " )
    print( "[fit__magneticMoment.py]     B0 :: {0}".format( popt[0] ) )
    print( "[fit__magneticMoment.py]     Br :: {0}".format( popt[1] ) )
    print()
    
    # ------------------------------------------------- #
    # --- [3] save as a figure                      --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf
    config  = lcf.load__config()
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=zval, yAxis=bval, linestyle="none", marker="x" )
    fig.add__plot( xAxis=zfit, yAxis=bfit, linestyle=":" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ========================================================= #
# ===  magneticMoment Function                          === #
# ========================================================= #

def eq__magneticMoment( x, b0, b1 ):
    vol  = 6.22e-7
    ret  = b0 + ( b1 * vol / np.pi ) / x**3 * 0.5
    return( ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    fit__magneticMoment()
