import numpy as np

# ========================================================= #
# ===  regenerator_like_profile.py                      === #
# ========================================================= #

def regenerator_like_profile( r1=0.9, r2=1.1, p1=250.0, p2=275.0, B0=1.0, save=True, cMap=True, \
                              x1Min=-0.4, x1Max=+0.4, x2Min=-1.2, x2Max=-0.8, LI=61, LJ=61, \
                              outFile="out.dat", pngFile="out.png" ):

    x_, y_, z_, b_ = 0, 1, 2, 5
    
    # ------------------------------------------------- #
    # --- [1] grid making                           --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ x1Min, x1Max, LI ]
    x2MinMaxNum = [ x2Min, x2Max, LJ ]
    x3MinMaxNum = [   0.0,   0.0,  1 ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    
    # ------------------------------------------------- #
    # --- [2] coordinate normalize                  --- #
    # ------------------------------------------------- #
    radii       = np.sqrt( ret[:,x_]**2 + ret[:,y_]**2 )
    theta       = np.arctan2( ret[:,y_], ret[:,x_] ) * 180.0 / np.pi
    theta[ np.where( theta < 0.0 ) ] = theta[ np.where( theta < 0.0 ) ] + 360.0

    rc, rl      = ( r2+r1 )*0.5, ( r2-r1 )*0.5
    pc, pl      = ( p2+p1 )*0.5, ( p2-p1 )*0.5
    r_norm      = ( radii - rc ) / rl
    p_norm      = ( theta - pc ) / pl

    r_norm[ np.where( r_norm < -1.0 ) ] = -1.0
    r_norm[ np.where( r_norm > +1.0 ) ] = +1.0
    p_norm[ np.where( p_norm < -1.0 ) ] = -1.0
    p_norm[ np.where( p_norm > +1.0 ) ] = +1.0

    # ------------------------------------------------- #
    # --- [3] regenerator like profile              --- #
    # ------------------------------------------------- #
    rFunc       = ( np.cos( 0.5*np.pi*r_norm ) )**2
    pFunc       = ( np.cos( 0.5*np.pi*p_norm ) )**2
    bfield      = rFunc*pFunc * B0

    Data        = np.zeros( (ret.shape[0],6) )
    Data[:,0:3] = np.copy( ret )
    Data[:,3:5] = 0.0
    Data[:,  5] = bfield
    
    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    if ( save ):
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=outFile, Data=Data )

    if ( cMap ):
        import nkUtilities.load__config   as lcf
        import nkUtilities.cMapTri        as cmt
        config                   = lcf.load__config()
        config["xTitle"]         = "X (m)"
        config["yTitle"]         = "Y (m)"
        config["cmp_xAutoRange"] = True
        config["cmp_yAutoRange"] = True
        cmt.cMapTri( xAxis=Data[:,x_], yAxis=Data[:,y_], cMap=Data[:,b_], \
                     pngFile=pngFile, config=config )
    return( Data )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    regenerator_like_profile()
