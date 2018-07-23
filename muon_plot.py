from muon_h import *

def makeMuonJetTypePlots(data):

    list_of_plots = []

    #initialize all the plots we're going to make for each pt bin and eta bin
    muon_pt_plot     = StackedPlot("Muon $p_T$",
                                  "$p_T$ [GeV/c]",
                                  np.linspace(0,450,50),
                                  True,
                                  True)

    muon_smt_plot    = StackedPlot("Muon SMT",
                                  "SMT",
                                  np.linspace(-1.1,1.1,50),
                                  True,
                                  True)

    muon_deltar_plot = StackedPlot("$\Delta R$($\mu$,jet)",
                                  "$\Delta R$",
                                  np.linspace(0,0.42,50),
                                  True,
                                  True)

    muon_ptfrac_plot = StackedPlot("${p_T}^{\mu} / {p_T}^{jet}$",
                                  "${p_T}^{\mu} / {p_T}^{jet}$",
                                  np.linspace(0,2,50),
                                  True,
                                  True)

    muon_ptrel_plot  = StackedPlot("Muon ${p_T}^{rel}$($\mu$,jet)",
                                  "${p_T}^{rel}$ [GeV/c]",
                                  np.linspace(0,450,50),
                                  True,
                                  True)

    muon_dzero_plot  = StackedPlot("Muon $d_0$",
                                  "$d_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True)

    muon_zzero_plot  = StackedPlot("Muon $z_0$",
                                  "$z_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True)

    """
    muon_dsig_plot   = StackedPlot("Muon $d_0 / \sigma_{d_0}$",
                                  "$d_0 / \sigma_{d_0}$",
                                  np.linspace(0,0.6,50),
                                  True,
                                  True)

    muon_zsig_plot   = StackedPlot("Muon $z_0 / \sigma_{z_0}$",
                                  "$z_0 / \sigma_{z_0}$",
                                  np.linspace(0,0.6,50),
                                  True,
                                  True)
    """

    #now loop over each type of jet
    for jt in JetType:

        #we will fill these lists with the corresponding data for the selected jet type
        muon_pt     = []
        muon_smt    = []
        muon_deltar = []
        muon_ptfrac = []
        muon_ptrel  = []
        muon_dzero  = []
        muon_zzero  = []
        #muon_dsig   = []
        #muon_zsig   = []

        #for each event in the dataset
        for i in range(data.size):
            if i%10000==0: print i
            #for each jet in that event
            for jet in range(data[i]['jet_pt'].size):
                if (
                    #Nicole's jet cuts
                    data[i]['jet_LabDr_HadF'][jet] == JetType[jt]["pdgId"] and
                    data[i]['jet_pt'][jet] > 20*GeV and
                    abs(data[i]['jet_eta'][jet]) < 2.5 and
                    data[i]['jet_aliveAfterOR'][jet] == 1 and
                    data[i]['jet_aliveAfterORmu'][jet] == 1 and
                    ((data[i]['jet_pt'][jet] > 60) or (abs(data[i]['jet_eta'][jet]) > 2.4) or (data[i]['jet_JVT'] > 0.59)) and

                    #Muon cuts
                    data[i]['jet_mu_pt'][jet] > 1*GeV and
                    abs(data[i]['jet_mu_eta'][jet]) < 2.5
                   ):
                            #append all the relevant data to the lists we made earlier
                            muon_pt.append(data[i]['jet_mu_pt'][jet]/GeV)

                            muon_smt.append(data[i]['jet_mu_smt'][jet])

                            muon_deltar.append(data[i]['jet_mu_dR'][jet])

                            muon_ptfrac.append(data[i]['jet_mu_pt'][jet]/data[i]['jet_pt'][jet])

                            muon_ptrel.append(data[i]['jet_mu_pTrel'][jet]/GeV)

                            muon_dzero.append(data[i]['jet_mu_d0'][jet])

                            muon_zzero.append(data[i]['jet_mu_z0'][jet])

                            #muon_dsig.append(data[i]['jet_trk_ip3d_d0sig'][jet][trk])

                            #muon_zsig.append(data[i]['jet_trk_ip3d_z0sig'][jet][trk])

        #give all our newly created histograms to the plots we initialized
        muon_pt_plot.appendHisto(muon_pt, JetType[jt])
        muon_smt_plot.appendHisto(muon_smt, JetType[jt])
        muon_deltar_plot.appendHisto(muon_deltar, JetType[jt])
        muon_ptfrac_plot.appendHisto(muon_ptfrac, JetType[jt])
        muon_ptrel_plot.appendHisto(muon_ptrel, JetType[jt])
        muon_dzero_plot.appendHisto(muon_dzero, JetType[jt])
        muon_zzero_plot.appendHisto(muon_dzero, JetType[jt])
        #muon_dsig_plot.appendHisto(muon_dsig, JetType[jt])
        #muon_zsig_plot.appendHisto(muon_zsig, JetType[jt])

    #add each new plot to the list of plots, which will be returned
    list_of_plots.append(muon_pt_plot)
    list_of_plots.append(muon_smt_plot)
    list_of_plots.append(muon_deltar_plot)
    list_of_plots.append(muon_ptfrac_plot)
    list_of_plots.append(muon_ptrel_plot)
    list_of_plots.append(muon_dzero_plot)
    list_of_plots.append(muon_zzero_plot)
    #list_of_plots.append(muon_dsig_plot)
    #list_of_plots.append(muon_zsig_plot)

    return list_of_plots

def printMuonPlots(plotList):
    for plot in plotList:
        plot.makePlot()
