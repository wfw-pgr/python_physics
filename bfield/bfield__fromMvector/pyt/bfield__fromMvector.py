import os, sys
import numpy as np


# ========================================================= #
# ===  bfield__fromMvector.py                           === #
# ========================================================= #

def bfield__fromMvector( rvec=None, mvec=None, vol=1.0 ):

    # --------------------------------------------------------- #
    # --                                                     -- #
    # -- B(r) = ( mu/4pi ) * ( 3 (rh.m) rh - m ) / |r|^3     -- #
    # --   rh = r / |r|                                      -- #
    # --    m = ( Br V ) / mu                                -- #
    # --                                                     -- #
    # -- B(r) = ( V/4pi ) * ( 3 (rh.Br) rh - Br ) / |r|^3    -- #
    # --                                                     -- #
    # -- r  :: rvec                                          -- #
    # -- Br :: mvec                                          -- #
    # --                                                     -- #
    # --------------------------------------------------------- #
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( rvec       is None ): sys.exit( "[bfield__fromMvector.py] rvec == ??? " )
    if ( mvec       is None ): sys.exit( "[bfield__fromMvector.py] mvec == ??? " )
    if ( type(rvec) is list ): rvec = np.array( rvec )
    if ( type(mvec) is list ): mvec = np.array( mvec )
    
    # ------------------------------------------------- #
    # --- [2] field calculation                     --- #
    # ------------------------------------------------- #
    coef   = vol / ( 4.0*np.pi )
    npt    = rvec.shape[0]
    mvec_  = np.repeat( mvec[None,:], npt, axis=0 )
    rnorm  = np.repeat( ( np.sqrt( np.sum( rvec**2, axis=1 ) ) )[:,None], 3, axis=1 )
    rhat   = rvec / rnorm
    rdotm  = np.repeat( ( np.sum( mvec_*rhat, axis=1 ) )[:,None], 3, axis=1 )
    bfield = coef * ( 3.0 * rhat * rdotm - mvec_ ) / rnorm**3
    return( bfield )



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    xvec = np.zeros( (91,) )
    yvec = np.zeros( (91,) )
    zvec = np.linspace(  0.030, 0.080, 91 )
    rvec = np.concatenate( [xvec[:,None],yvec[:,None],zvec[:,None],], axis=1 )
    mvec = np.array( [ 0.0, 0.0, 0.8 ] )
    vol  = 6.22e-7
    print( rvec )
    print( rvec.shape, mvec.shape )
    
    ret = bfield__fromMvector( rvec=rvec, mvec=mvec, vol=vol )
    print( ret )
