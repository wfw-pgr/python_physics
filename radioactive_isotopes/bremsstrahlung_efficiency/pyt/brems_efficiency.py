import numpy as np

# ========================================================= #
# ===  efficiencyOfBremsstrahlung                       === #
# ========================================================= #
def calc__efficiencyOfBremsstrahlung( Z=78.0, Eb=45.0, coef=6.0e-4 ):
    if ( type( Eb ) is float ): Eb = [ Eb ]
    if ( type( Eb ) is list  ): Eb = np.array( Eb )
    ret = ( coef * Z * Eb ) / ( 1.0 + ( coef * Z * Eb ) )
    return( ret )


# ========================================================= #
# ===  bremsstrahlungEfficiency                         === #
# ========================================================= #

def bremsstrahlungEfficiency():

    E_ = 0

    # ------------------------------------------------- #
    # --- [1] load config                           --- #
    # ------------------------------------------------- #
    import json
    inpFile = "dat/parameters.json"
    with open( inpFile, "r" ) as f:
        params  = json.load( f )
    Zs       = params["Zs"]
    if   ( params["energyMode"].lower() == "linspace" ):
        energies = np.linspace( params["Emin"], params["Emax"], params["nE"] )
    elif ( params["energyMode"].lower() == "list" ):
        energies = np.array( params["energyList"] )
        
    # ------------------------------------------------- #
    # --- [2] calculate bremsstrahlung efficiency   --- #
    # ------------------------------------------------- #
    stack  = []
    stack += [ energies[:,np.newaxis] ]
    for zh in Zs:
        stack += [ np.reshape( calc__efficiencyOfBremsstrahlung( Z=zh, Eb=energies ), (-1,1) ) ]
    Data = np.concatenate( stack, axis=1 )

    nData  = Data.shape[0]
    nElems = Data.shape[1] - 1

    # ------------------------------------------------- #
    # --- [3] save in file                          --- #
    # ------------------------------------------------- #
    elementsDict = { "Z=42":"Mo", "Z=73":"Ta", "Z=78":"Pt", "Z=79":"Au", "Z=92":"U" }
    names = [ "Energy(MeV)" ] + [ "Z={}".format( int(zh) ) for zh in params["Zs"] ]
    names = [ elementsDict[name] if ( name in elementsDict ) else name for name in names ]
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/bremsstrahlungEfficiency.dat"
    spf.save__pointFile( outFile=outFile, Data=Data, names=names )

    # ------------------------------------------------- #
    # --- [4] draw figure                           --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    pngFile                  = outFile.replace( "dat", "png" )
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["FigSize"]        = (4.5,4.5)
    config["plt_position"]   = [ 0.16, 0.16, 0.94, 0.94 ]
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["xTitle"]         = "Energy (MeV)"
    config["yTitle"]         = "Efficiency (%)"
    config["plt_xRange"]     = [ 0.0, 50.0 ]
    config["plt_yRange"]     = [ 0.0, 100.0 ]
    config["xMajor_Nticks"]  =  6
    config["yMajor_Nticks"]  = 11
    config["xMinor_nticks"]  = 2
    config["yMinor_nticks"]  = 2
    config["plt_marker"]     = "none"
    config["plt_markersize"] = 0.0
    config["plt_linestyle"]  = "-"
    config["plt_linewidth"]  = 2.0

    print( Data.shape )
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( nElems ):
        fig.add__plot( xAxis=Data[:,E_], yAxis=100.0*Data[:,ik+1], \
                       label=names[ik+1] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    bremsstrahlungEfficiency()

