import os, sys
import numpy    as np
import datetime as dtime
import nkUtilities.plot1D         as pl1
import nkUtilities.load__config   as lcf
import nkUtilities.configSettings as cfs

# ========================================================= #
# ===  apply__attenationCorrection.py                   === #
# ========================================================= #

def apply__attenationCorrection():

    time_format = "%Y-%m-%d %H:%M:%S"
    text_format = "{0:>30} = {1}\n"
    
    # ------------------------------------------------- #
    # --- [1] load parameters                       --- #
    # ------------------------------------------------- #
    import json, re
    inpFile = "dat/parameters.jsonc"
    with open( inpFile, "r" ) as f:
        text   = re.sub(r'/\*[\s\S]*?\*/|//.*', '', f.read() )
        params = json.loads( text )

    # ------------------------------------------------- #
    # --- [2] calculation of time and dates         --- #
    # ------------------------------------------------- #
    Thalf1_sec   = unit__halfLifeTime_second( unit=params["halflife1.unit"], \
                                              value=params["halflife1"] )
    Thalf2_sec   = unit__halfLifeTime_second( unit=params["halflife2.unit"], \
                                              value=params["halflife2"] )
    lamb1        = np.log( 2.0 ) / ( Thalf1_sec )
    lamb2        = np.log( 2.0 ) / ( Thalf2_sec )
    Tmax         = np.log( lamb1 / lamb2 ) / ( lamb1 - lamb2 )
    T_beam_start = dtime.datetime.strptime( params["T.beam.start"], time_format )
    T_beam_end   = dtime.datetime.strptime( params["T.beam.end"]  , time_format )
    T_HPGe_start = dtime.datetime.strptime( params["T.HPGe.start"], time_format )
    T_HPGe_end   = dtime.datetime.strptime( params["T.HPGe.end"]  , time_format )
    T_HPGe_ave   =   T_HPGe_start + 0.5*( T_HPGe_end   - T_HPGe_start )
    Tstart       = ( T_HPGe_start - T_beam_end ).total_seconds()
    Tend         = ( T_HPGe_end   - T_beam_end ).total_seconds()
    Tmean        =   0.5*( Tstart + Tend )
    T_radi_max   = T_beam_end + dtime.timedelta( seconds=Tmax )
    Tmax_days    = Tmax    / ( 24*60*60 )
    Tmean_days   = Tmean   / ( 24*60*60 )
    Tstart_days  = Tstart / ( 24*60*60 )
    Tend_days    = Tend   / ( 24*60*60 )
    
    # ------------------------------------------------- #
    # --- [3] calculation attenation Correction     --- #
    # ------------------------------------------------- #
    numerator    = ( np.exp( - lamb1 * Tmax  ) - np.exp( -lamb2 * Tmax  ) )
    denominator  = ( np.exp( - lamb1 * Tmean ) - np.exp( -lamb2 * Tmean ) )
    atteFactor   = numerator / denominator
    results      = { "lambda.1":lamb1, "lambda.2":lamb2,
                     "Tmax.sec":Tmax, "Tmean.sec":Tmean, \
                     "Tmax.day":Tmax_days, "Tmean.day":Tmean_days, \
                     "Tstart.day":Tstart_days, "Tend.day":Tend_days, \
                     "T_HPGe_start":dtime.datetime.strftime( T_HPGe_start, time_format ),\
                     "T_HPGe_end":  dtime.datetime.strftime( T_HPGe_end  , time_format ),\
                     "T_HPGe_ave":dtime.datetime.strftime  ( T_HPGe_ave  , time_format ),\
                     "T_radi_max":T_radi_max, \
                     "attenationCorrectionFactor":atteFactor }

    # ------------------------------------------------- #
    # --- [4] display                               --- #
    # ------------------------------------------------- #
    texts      = "\n"
    for key,val in results.items():
        texts += text_format.format( key, val )
    texts     += "\n"
    print( texts )
    with open( params["outFile"], "w" ) as f:
        f.write( texts )

    # ------------------------------------------------- #
    # --- [5] draw figures                          --- #
    # ------------------------------------------------- #
    draw__figures( params=params, results=results )
    return( atteFactor, texts )


# ========================================================= #
# ===  unit__halfLifeTime_second                        === #
# ========================================================= #
def unit__halfLifeTime_second( unit=None, value=None ):
    
    if   ( unit.lower() == "y" ):
        ret = value * 365*24*60*60.0
    elif ( unit.lower() == "d" ):
        ret = value *     24*60*60.0
    elif ( unit.lower() == "h" ):
        ret = value *        60*60.0
    elif ( unit.lower() == "m" ):
        ret = value *           60.0
    elif ( unit.lower() == "s" ):
        ret = value
    else:
        print( "[estimate__RIproduction.py] unknown unit :: {} ".format( unit ) )
        sys.exit()
    return( ret )


# ========================================================= #
# ===  draw__figures                                    === #
# ========================================================= #
def draw__figures( params=None, results=None ):

    min_,max_,num_ = 0, 1, 2
    day            = 24 * 60 * 60
    
    # ------------------------------------------------- #
    # --- [1] calculation and expansion             --- #
    # ------------------------------------------------- #
    tRange  = params["graph.time.MinMaxNum"]
    lamb1   = results["lambda.1"]
    lamb2   = results["lambda.2"]
    time    = np.linspace( tRange[min_], tRange[max_], tRange[num_] )
    time_P  = np.array( [ results["Tstart.day"], results["Tmean.day"], results["Tend.day"] ] )
    atte_A  = np.exp( - lamb1 * time   * day )
    atte_B  = np.exp( - lamb1 * time   * day ) - np.exp( - lamb2 * time   * day )
    atte_P  = np.exp( - lamb1 * time_P * day ) - np.exp( - lamb2 * time_P * day )
    atte_B  = atte_B * ( lamb2 / ( lamb2 - lamb1 ) )
    atte_P  = atte_P * ( lamb2 / ( lamb2 - lamb1 ) )
    label_A = "Ra-225"
    label_B = "Ac-225"
    label_P = "HPGe [start,mean,end] "
    
    # ------------------------------------------------- #
    # --- [2] configuration                         --- #
    # ------------------------------------------------- #
    x_,y_                    = 0, 1
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["FigSize"]        = (4.5,4.5)
    config["plt_position"]   = [ 0.16, 0.16, 0.94, 0.94 ]
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]
    config["xMajor_Nticks"]  = 11
    config["yMajor_Nticks"]  = 11
    config["plt_marker"]     = "none"
    config["plt_markersize"] = 3.0
    config["plt_linestyle"]  = "-"
    config["plt_linewidth"]  = 1.0
    config["xTitle"]         = "elapsed days (d)"
    config["yTitle"]         = "$A/A_0$"

    # ------------------------------------------------- #
    # --- [3] plot                                  --- #
    # ------------------------------------------------- #
    fig     = pl1.plot1D( config=config, pngFile=params["pngFile"] )
    fig.add__plot( xAxis=time  , yAxis=atte_A, label=label_A )
    fig.add__plot( xAxis=time  , yAxis=atte_B, label=label_B )
    fig.add__plot( xAxis=time_P, yAxis=atte_P, label=label_P, \
                   marker="o", markersize=2.0, linestyle="none" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    apply__attenationCorrection()

