import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display__temperature                             === #
# ========================================================= #
def display__temperature():

    x_,y1_,y2_   = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/residuals.dat"
    pngFile = "png/temperature.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Number of iterations"
    config["yTitle"]         = "Temperature (" + r"$^\circ$" + "C)"
    config["plt_position"]   = [ 0.12, 0.18, 0.88,0.94]
    config["FigSize"]        = (6.0,5.0)
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [    0, 10  ]
    config["plt_yRange"]     = [ 290, 360  ]
    config["xMajor_Nticks"]  = 11
    config["yMajor_Nticks"]  =  8
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMinor_sw"]      = False
    config["ax2.ylog"]       = True
    config["ax2.yTitle"]     = "convergence"
    config["ax2.yMajor.auto"] = False
    config["ax2.yMajor.ticks"] = [ 10.0**(ik) for ik in np.linspace( -6, +1, 8 ) ]
    config["ax2.yAutoRange"]   = False
    config["ax2.yRange"]       = [ 1.e-6, 1.e+1 ]

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    import matplotlib.pyplot as plt
    colors = plt.get_cmap()
    print( colors(0) )
    fig.add__plot ( xAxis=Data[:,x_], yAxis=Data[:,y1_], color="C0", marker="o" )
    fig.add__plot2( xAxis=Data[:,x_], yAxis=Data[:,y2_], color="C1", marker="o" )
    fig.set__axis()
    fig.save__figure()



# ========================================================= #
# ===  display__residuals                               === #
# ========================================================= #
def display__residuals():

    x_,y_   = 0, 2

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/residuals.dat"
    pngFile = "png/residuals.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Number of iterations"
    config["yTitle"]         = "Convergence"
    config["plt_position"]   = [ 0.18, 0.18, 0.94,0.94]
    config["FigSize"]        = (5.0,5.0)
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_ylog"]       = True
    config["plt_xRange"]     = [    0, 10  ]
    config["xMajor_auto"]    = False
    config["yMajor_auto"]    = False
    config["xMajor_ticks"]   = np.linspace( 0, 10, 11 )
    config["yMajor_ticks"]   = [ 10**( ik ) for ik in np.linspace( -6, 1, 8 ) ]
    config["plt_yRange"]     = [ 1e-6, 1e+1]
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMinor_sw"]      = False

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,y_], marker="o" )
    fig.set__axis()
    fig.save__figure()


# ========================================================= #
# ===  display__viscosity_thermalConductivity           === #
# ========================================================= #
def display__viscosity_thermalConductivity():

    x_,y_   = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config   = lcf.load__config()
    datFile1 = "dat/thermalConductivity.dat"
    datFile2 = "dat/viscosity.dat"
    pngFile  = "png/viscosity_thermalConductivity.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data1       = lpf.load__pointFile( inpFile=datFile1, returnType="point" )
    Data2       = lpf.load__pointFile( inpFile=datFile2, returnType="point" )
    Data1[:,y_] = Data1[:,y_] * 1e-3
    Data1       = Data1[ np.where( Data1[:,x_] < 850.0 ) ]
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Temperature (" + r"$^\circ$" + "C)"
    config["yTitle"]         = "viscosity " + r"$\nu \ \mathrm{(m^2/s)}$"
    config["plt_position"]   = [ 0.18, 0.18, 0.94,0.94]
    config["FigSize"]        = (5.0,5.0)
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_ylog"]       = True
    config["plt_xRange"]     = [ -150, 850 ]
    config["plt_yRange"]     = [ 1e-6, 1e-3]
    config["xMajor_auto"]    = False
    config["yMajor_auto"]    = False
    config["xMajor_ticks"]   = np.linspace( -100, +800, 10 )
    config["yMajor_ticks"]   = [ 10**( ik ) for ik in np.linspace( -6, -3, 4 ) ]
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMinor_sw"]      = False

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data1[:,x_], yAxis=Data1[:,y_], marker="o", label=r"$\lambda$" )
    fig.add__plot( xAxis=Data2[:,x_], yAxis=Data2[:,y_], marker="o", label=r"$\nu$" )
    fig.set__axis()
    fig.add__legend()
    fig.save__figure()


# ========================================================= #
# ===  display__HilpertCoeff                            === #
# ========================================================= #
def display__HilpertCoeff():

    x_,y_   = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config   = lcf.load__config()
    datFile  = "dat/HilpertModel.dat"
    pngFile  = "png/HilpertCoeff.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data        = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    xAxis1      = Data[:,0]
    xAxis2      = Data[:,1]
    cAxis       = Data[:,2]
    mAxis       = Data[:,3]
    xAxis_      = np.concatenate( [xAxis1[np.newaxis,:],xAxis2[np.newaxis,:]], axis=0 )
    cAxis_      = np.repeat( cAxis[np.newaxis,:], 2, axis=0 )
    mAxis_      = np.repeat( mAxis[np.newaxis,:], 2, axis=0 )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Re"
    config["yTitle"]         = "C, m"
    config["plt_position"]   = [ 0.18, 0.18, 0.94,0.94]
    config["FigSize"]        = (5.0,5.0)
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xlog"]       = True
    config["plt_xRange"]     = [ 0.1, 100000 ]
    config["plt_yRange"]     = [ -0.1, 1.1    ]
    config["xMajor_auto"]    = False
    config["yMajor_auto"]    = False
    config["xMajor_ticks"]   = [ 10**( ik ) for ik in np.linspace( -1, 5, 6 ) ]
    config["yMajor_ticks"]   = np.linspace( 0, 1.0, 11 )
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMinor_sw"]      = False

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( xAxis_.shape[1] ):
        fig.add__plot( xAxis=xAxis_[:,ik], yAxis=cAxis_[:,ik], \
                       marker="o", label="C(Re)", color="royalblue" )
        fig.add__plot( xAxis=xAxis_[:,ik], yAxis=mAxis_[:,ik], \
                       marker="o", label="m(Re)", color="orange"    )
    fig.set__axis()
    # fig.add__legend()
    fig.save__figure()




# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    # display__residuals()
    display__temperature()
    # display__viscosity_thermalConductivity()
    # display__HilpertCoeff()
