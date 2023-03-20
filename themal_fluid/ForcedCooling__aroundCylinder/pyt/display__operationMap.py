import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display__flowRate():

    x_,y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config   = lcf.load__config()
    datFiles = [ "dat/flow_6kW.dat", "dat/flow_9kW.dat", \
                 "dat/flow_12kW.dat", "dat/flow_15kW.dat" ]
    labels   = [ "6 kW", "9 kW", "12 kW", "15 kW" ]
    pngFile  = "png/flow_scan.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data_list = [ lpf.load__pointFile( inpFile=datFile ) for datFile in datFiles ]
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Pump flow rate (L/min)"
    config["yTitle"]         = "Temperature (" + r"$^\circ$" + "C)"
    config["FigSize"]        = (5,5)
    config["plt_position"]   = [0.14,0.14,0.94,0.94]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [0.0, 130.0]
    config["plt_yRange"]     = [0.0, 1200.0]
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMajor_Nticks"]  = 14
    config["yMajor_Nticks"]  = 13

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    for ik,Data in enumerate( Data_list ):
        fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,y_], label=labels[ik], \
                       marker="o" )
    fig.set__axis()
    fig.add__legend()
    fig.save__figure()

    
# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display__power():

    x_,h_,t_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config  = lcf.load__config()
    datFile = "dat/power_scan.dat"
    pngFile = "png/power_scan.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data  = lpf.load__pointFile( inpFile=datFile, returnType="point" )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Beam power (kW)"
    config["yTitle"]         = "Temperature (" + r"$^\circ$" + "C)"
    config["FigSize"]        = (5,5)
    config["plt_position"]   = [0.14,0.14,0.94,0.94]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [0.0, 20.0]
    config["plt_yRange"]     = [0.0, 1000.0]
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMajor_Nticks"]  = 11
    config["yMajor_Nticks"]  = 11

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,t_], marker="o" )
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display__flowRate()
    display__power()

