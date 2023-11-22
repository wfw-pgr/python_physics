import numpy as np

import nkUtilities.plot1D         as pl1
import nkUtilities.load__config   as lcf
import nkUtilities.configSettings as cfs
x_,s_,e_                 = 0, 1, 2
pngFile                  = "png/statistic_error.png"
config                   = lcf.load__config()
config                   = cfs.configSettings( configType="plot.def", config=config )
config["FigSize"]        = (4.5,4.5)
config["plt_position"]   = [ 0.16, 0.16, 0.94, 0.94 ]
config["plt_xAutoRange"] = False
config["plt_yAutoRange"] = False
config["plt_xRange"]     = [ 1.0, +1.0e6 ]
config["xMajor_Nticks"]  = 6
config["plt_marker"]     = "o"
config["plt_markersize"] = 3.0
config["plt_linestyle"]  = "-"
config["plt_linewidth"]  = 2.0
config["plt_xlog"]       = True
config["plt_ylog"]       = True
config["xTitle"]         = "N"

s          = np.linspace( 1.0, 10.0, 10 )
xAxis_list = [ s * 10**(i-1) for i in ( np.arange( 6 )+1.0 )  ]
xAxis      = np.concatenate( xAxis_list )
sAxis      = np.sqrt( xAxis )
eAxis      = np.sqrt( xAxis ) / xAxis
print( xAxis.shape, sAxis.shape, eAxis.shape )
Data       = np.concatenate( [ xAxis[:,np.newaxis], sAxis[:,np.newaxis], eAxis[:,np.newaxis] ], axis=1 )

pngFile1                 = "png/stddev.png"
config["plt_xlog"]       = True
config["plt_ylog"]       = True
config["yTitle"]         = "$\sigma$"
config["plt_yRange"]     = [ 1.0, +1.0e3 ]
config["yMajor_Nticks"]  = 4
fig     = pl1.plot1D( config=config, pngFile=pngFile1 )
fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,s_] )
fig.set__axis()
fig.save__figure()

pngFile2                 = "png/relative_error.png"
config["plt_xlog"]       = True
config["plt_ylog"]       = True
config["yTitle"]         = "Relative Error (%)"
# config["plt_yRange"]     = [ 1.0e-1, +1.0e+2 ]
config["plt_yRange"]     = [ 5.0e-2, +2.0e+2 ]
config["yMajor_ticks"]   = [ 1.0e-1, 1.0e0, 1.0e1, +1.0e2 ]
config["yMajor_Nticks"]  = 5
fig     = pl1.plot1D( config=config, pngFile=pngFile2 )
fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,e_]*100.0 )
fig.set__axis()
fig.save__figure()

import nkUtilities.save__pointFile as spf
outFile   = "dat/statistic_error.dat"
spf.save__pointFile( outFile=outFile, Data=Data )
