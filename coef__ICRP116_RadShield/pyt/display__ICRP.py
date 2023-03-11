import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():

    x1_,y1_ = 0, 6
    x2_,y2_ = 0, 6
    x3_,y3_ = 0, 3
    x4_,y4_ = 0, 6

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config   = lcf.load__config()
    datFile1 = "dat/photon_ICRP116.dat"
    datFile2 = "dat/proton_ICRP116.dat"
    datFile3 = "dat/electron_ICRP116.dat"
    datFile4 = "dat/neutron_ICRP116.dat"
    pngFile  = "png/ICRP116.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data1  = lpf.load__pointFile( inpFile=datFile1, returnType="point" )
    Data2  = lpf.load__pointFile( inpFile=datFile2, returnType="point" )
    Data3  = lpf.load__pointFile( inpFile=datFile3, returnType="point" )
    Data4  = lpf.load__pointFile( inpFile=datFile4, returnType="point" )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Energy (MeV)"
    config["yTitle"]         = "Dose Conversion Coefficient ICRP116 (pSv cm2)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [1.e-9,1.e+4]
    config["plt_yRange"]     = [1.e-2,1.e+4]
    config["plt_xlog"]       = True
    config["plt_ylog"]       = True
    config["plt_linewidth"]  = 1.0
    config["plt_linestyle"]  = "-"
    config["xMajor_Nticks"]  = 11
    config["xMinor_Nticks"]  = 10
    config["yMajor_Nticks"]  = 11

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=Data1[:,x1_], yAxis=Data1[:,y1_], label="photon"   )
    fig.add__plot( xAxis=Data2[:,x2_], yAxis=Data2[:,y2_], label="proton"   )
    fig.add__plot( xAxis=Data3[:,x3_], yAxis=Data3[:,y3_], label="electron" )
    fig.add__plot( xAxis=Data4[:,x4_], yAxis=Data4[:,y4_], label="neutron"  )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

