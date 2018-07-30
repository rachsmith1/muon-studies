from util import *

def makePlots(data, jetName, muonParentName):

    #first assign the pdgid of the jet to the name given by the user
    jetPdgId = 0
    if jetName == "b jets": jetPdgId = 5
    elif jetName == "c jets": jetPdgId = 4
    elif jetName == "light jets": jetPdgId = 0
    elif jetName == "\\tau jets": jetPdgId = 15

    #append all plots to the list so that they can be recursively plotted
    list_of_plots = []

    #define plots
    muon_pt_plot     = StackedPlot("{}, muon parent is {}: Muon $p_T$".format(jetName, muonParentName),
                                  "$p_T$ [GeV/c]",
                                  np.linspace(0,150,50),
                                  True,
                                  True)

    muon_smt_plot    = StackedPlot("{}, muon parent is {}: Muon SMT".format(jetName, muonParentName),
                                  "SMT",
                                  np.linspace(-1.1,1.1,50),
                                  True,
                                  True)

    muon_deltar_plot = StackedPlot("{}, muon parent is {}:".format(jetName, muonParentName) + " $\Delta R$($\mu$,jet)",
                                  "$\Delta R$",
                                  np.linspace(0,0.42,50),
                                  True,
                                  True)

    muon_ptfrac_plot = StackedPlot("{}, muon parent is {}:".format(jetName, muonParentName) + " ${p_T}^{\mu} / {p_T}^{jet}$",
                                  "${p_T}^{\mu} / {p_T}^{jet}$",
                                  np.linspace(0,5,50),
                                  True,
                                  True)

    muon_ptrel_plot  = StackedPlot("{}, muon parent is {}:".format(jetName, muonParentName) + "${p_T}^{rel}$($\mu$,jet)",
                                  "${p_T}^{rel}$ [GeV/c]",
                                  np.linspace(0,250,50),
                                  True,
                                  True)

    muon_dzero_plot  = StackedPlot("{}, muon parent is {}: Muon $d_0$".format(jetName, muonParentName),
                                  "$d_0$ [mm]",
                                  np.linspace(0,20,50),
                                  True,
                                  True)

    muon_zzero_plot  = StackedPlot("{}, muon parent is {}: Muon $z_0$".format(jetName, muonParentName),
                                  "$z_0$ [mm]",
                                  np.linspace(0,50,50),
                                  True,
                                  True)

    muon_qoverp_plot = StackedPlot("{}, muon parent is {}: Muon $q/p$ ratio".format(jetName, muonParentName),
                                  "$q/p$ [1/(GeV/c)]",
                                  np.linspace(-25000000,25000000,50),
                                  True,
                                  True)

    dZeroVSzZero_plot = TwoDimensionalPlot(
                                  "{}, muon parent is {}: $d_0$ v. $z_0$".format(jetName, muonParentName),
                                  "$d_0$ [mm]",
                                  "$z_0$ [mm]",
                                  np.linspace(-5,5,50),
                                  np.linspace(-5,5,50))

    relIP_plot = BarPlot("{}, muon parent is {}: IP placement".format(jetName, muonParentName))

    #we want jets of a certain flavour and muons with a certain parent
    data["jet_mu_parent_name"] = [DefineParticle(p) for p in data.jet_mu_parent_pdgid]
    df_muParentChoice = data[ (data.jet_mu_parent_name == muonParentName) & (data.jet_LabDr_HadF == jetPdgId) ]

    ipDescPos = {"name": "$d_0 > 0$ and $z_0 > 0$", "color": "red"}
    ipDescNeg = {"name": "$d_0 \leq 0$ and $z_0 \leq 0$", "color": "blue"}

    #stacked plots
    muon_pt_plot.appendHisto([x/GeV for x in df_muParentChoice["jet_mu_pt"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]],   ipDescPos)
    muon_pt_plot.appendHisto([x/GeV for x in df_muParentChoice["jet_mu_pt"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]], ipDescNeg)

    muon_smt_plot.appendHisto(df_muParentChoice["jet_mu_smt"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)],   ipDescPos)
    muon_smt_plot.appendHisto(df_muParentChoice["jet_mu_smt"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)], ipDescNeg)

    muon_deltar_plot.appendHisto(df_muParentChoice["jet_mu_dR"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)],   ipDescPos)
    muon_deltar_plot.appendHisto(df_muParentChoice["jet_mu_dR"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)], ipDescNeg)

    muon_ptfrac_plot.appendHisto(df_muParentChoice["jet_mu_pt"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]/df_muParentChoice["jet_pt_orig"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)],     ipDescPos)
    muon_ptfrac_plot.appendHisto(df_muParentChoice["jet_mu_pt"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]/df_muParentChoice["jet_pt_orig"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)], ipDescNeg)

    muon_ptrel_plot.appendHisto([x/GeV for x in df_muParentChoice["jet_mu_pTrel"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]],   ipDescPos)
    muon_ptrel_plot.appendHisto([x/GeV for x in df_muParentChoice["jet_mu_pTrel"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]], ipDescNeg)

    muon_dzero_plot.appendHisto([abs(x) for x in df_muParentChoice["jet_mu_d0"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]],   ipDescPos)
    muon_dzero_plot.appendHisto([abs(x) for x in df_muParentChoice["jet_mu_d0"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]], ipDescNeg)

    muon_zzero_plot.appendHisto([abs(x) for x in df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]],   ipDescPos)
    muon_zzero_plot.appendHisto([abs(x) for x in df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]], ipDescNeg)

    muon_qoverp_plot.appendHisto([x*GeV for x in df_muParentChoice["jet_mu_qOverPratio"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)]],   ipDescPos)
    muon_qoverp_plot.appendHisto([x*GeV for x in df_muParentChoice["jet_mu_qOverPratio"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)]], ipDescNeg)

    #2d histograms
    dZeroVSzZero_plot.appendHisto(df_muParentChoice["jet_mu_d0"], df_muParentChoice["jet_mu_z0"])

    #bar graphs
    dpzp = len(df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]>0)])
    dpzn = len(df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]>0) & (df_muParentChoice["jet_mu_z0"]<=0)])
    dnzp = len(df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]>0)])
    dnzn = len(df_muParentChoice["jet_mu_z0"][(df_muParentChoice["jet_mu_d0"]<=0) & (df_muParentChoice["jet_mu_z0"]<=0)])
    relIP_plot.addData([dpzp, dpzn, dnzp, dnzn],["$d_0 > 0$ and $z_0 > 0$",
                                                 "$d_0 > 0$ and $z_0 \leq 0$",
                                                 "$d_0 \leq 0$ and $z_0 > 0$",
                                                 "$d_0 \leq 0$ and $z_0 \leq 0$"])

    #append all plots to the list of plots assigned earlier
    list_of_plots.append(muon_pt_plot)
    list_of_plots.append(muon_smt_plot)
    list_of_plots.append(muon_deltar_plot)
    list_of_plots.append(muon_ptfrac_plot)
    list_of_plots.append(muon_ptrel_plot)
    list_of_plots.append(muon_dzero_plot)
    list_of_plots.append(muon_zzero_plot)
    list_of_plots.append(muon_qoverp_plot)
    list_of_plots.append(dZeroVSzZero_plot)
    list_of_plots.append(relIP_plot)

    #return the list of plots so they can be recursivley drawn
    return list_of_plots

#recursively draws plots in a list of plots
def printPlots(plotList):
    for plot in plotList:
        plot.printPlot()
