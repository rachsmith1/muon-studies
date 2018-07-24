from muon_h import *

def DefineParticle(pdgid):
    if      pdgid==211: return "pi +/-"
    elif pdgid==999: return "pileup"
    elif pdgid==24:  return "W +/-"
    elif pdgid==15:  return "$\\tau$ +/-"
    elif pdgid==22:  return "photon"
    elif np.floor(pdgid/1000)==3 or np.floor(pdgid/100)==3 or pdgid==130 or pdgid==221 or pdgid==223 or pdgid==333 or pdgid==113 or pdgid==331:
        return "light/strange meson"
    elif np.floor(pdgid/1000)==5 or np.floor(pdgid/100)==5 or np.floor(pdgid/1000)==4 or np.floor(pdgid/100)==4:
        return "b/c hadron"
    else:
        return "N/A"

def makeMuonJetTypePlots(data):

    list_of_plots = []

    #initialize all the plots we're going to make for each pt bin and eta bin
    muon_pt_plot     = StackedPlot("Muon $p_T$",
                                  "$p_T$ [GeV/c]",
                                  np.linspace(0,250,50),
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
                                  np.linspace(0,250,50),
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

    muon_qoverp_plot = StackedPlot("$q$ over $p$ ratio",
                                  "$q/p$ [GeV/c]${}^{-1}$",
                                  np.linspace(-25000000,25000000,50),
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
        muon_qoverp = []
        #muon_dsig   = []
        #muon_zsig   = []

        #for each event in the dataset
        for i in range(data.size):
        #for i in range(100000):
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

                            sign_d0 = np.sign(np.sin(data[i]['jet_phi'][jet] - data[i]['jet_mu_phi'][jet]) * data[i]['jet_mu_d0'][jet])
                            sign_z0 = np.sign((data[i]['jet_eta'][jet] - data[i]['jet_mu_eta'][jet]) * data[i]['jet_mu_z0'][jet])
                            signed_d0 = abs(data[i]['jet_mu_d0'][jet]) * sign_d0
                            signed_z0 = abs(data[i]['jet_mu_z0'][jet]) * sign_z0
                            muon_dzero.append(signed_d0)
                            muon_zzero.append(signed_z0)

                            muon_qoverp.append(data[i]['jet_mu_qOverPratio'][jet]*GeV)

                            #muon_dsig.append(data[i]['jet_trk_ip3d_d0sig'][jet][trk])

                            #muon_zsig.append(data[i]['jet_trk_ip3d_z0sig'][jet][trk])

        #give all our newly created histograms to the plots we initialized
        muon_pt_plot.appendHisto(muon_pt, JetType[jt])
        muon_smt_plot.appendHisto(muon_smt, JetType[jt])
        muon_deltar_plot.appendHisto(muon_deltar, JetType[jt])
        muon_ptfrac_plot.appendHisto(muon_ptfrac, JetType[jt])
        muon_ptrel_plot.appendHisto(muon_ptrel, JetType[jt])
        muon_dzero_plot.appendHisto(muon_dzero, JetType[jt])
        muon_zzero_plot.appendHisto(muon_zzero, JetType[jt])
        muon_qoverp_plot.appendHisto(muon_qoverp, JetType[jt])
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
    list_of_plots.append(muon_qoverp_plot)
    #list_of_plots.append(muon_dsig_plot)
    #list_of_plots.append(muon_zsig_plot)

    return list_of_plots

def makeMuonLightFlavourPlots(data):

    list_of_plots = []

    #initialize all the plots we're going to make for each pt bin and eta bin
    muon_pt_plot     = StackedPlot("Light-flavoured jets: Muon $p_T$",
                                  "$p_T$ [GeV/c]",
                                  np.linspace(0,250,50),
                                  True,
                                  True)

    muon_smt_plot    = StackedPlot("Light-flavoured jets: Muon SMT",
                                  "SMT",
                                  np.linspace(-1.1,1.1,50),
                                  True,
                                  True)

    muon_deltar_plot = StackedPlot("Light-flavoured jets: $\Delta R$($\mu$,jet)",
                                  "$\Delta R$",
                                  np.linspace(0,0.42,50),
                                  True,
                                  True)

    muon_ptfrac_plot = StackedPlot("Light-flavoured jets: ${p_T}^{\mu} / {p_T}^{jet}$",
                                  "${p_T}^{\mu} / {p_T}^{jet}$",
                                  np.linspace(0,2,50),
                                  True,
                                  True)

    muon_ptrel_plot  = StackedPlot("Light-flavoured jets: Muon ${p_T}^{rel}$($\mu$,jet)",
                                  "${p_T}^{rel}$ [GeV/c]",
                                  np.linspace(0,250,50),
                                  True,
                                  True)

    muon_dzero_plot  = StackedPlot("Light-flavoured jets: Muon $d_0$",
                                  "$d_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True)

    muon_zzero_plot  = StackedPlot("Light-flavoured jets: Muon $z_0$",
                                  "$z_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True)

    muon_qoverp_plot = StackedPlot("Light-flavoured jets: $q$ over $p$ ratio",
                                  "$q/p$ [GeV/c]${}^{-1}$",
                                  np.linspace(-25000000,25000000,50),
                                  True,
                                  True)

    ParentPdgId = OrderedDict()
    cmap = plt.get_cmap('gnuplot')
    colorList = ["red","orange","green","blue","teal","indigo","black","violet"]
    colorPlace = 0

    #for each event in the dataset
    for i in range(data.size):
    #for i in range(10000):
        if i%10000==0: print i
        #for each jet in that event
        for jet in range(data[i]['jet_pt'].size):
            if (
                #Nicole's jet cuts
                data[i]['jet_LabDr_HadF'][jet] == 0 and
                data[i]['jet_pt'][jet] > 20*GeV and
                abs(data[i]['jet_eta'][jet]) < 2.5 and
                data[i]['jet_aliveAfterOR'][jet] == 1 and
                data[i]['jet_aliveAfterORmu'][jet] == 1 and
                ((data[i]['jet_pt'][jet] > 60) or (abs(data[i]['jet_eta'][jet]) > 2.4) or (data[i]['jet_JVT'] > 0.59)) and
                #Muon cuts
                data[i]['jet_mu_pt'][jet] > 1*GeV and
                abs(data[i]['jet_mu_eta'][jet]) < 2.5
               ):
                    sign_d0 = np.sign(np.sin(data[i]['jet_phi'][jet] - data[i]['jet_mu_phi'][jet]) * data[i]['jet_mu_d0'][jet])
                    sign_z0 = np.sign((data[i]['jet_eta'][jet] - data[i]['jet_mu_eta'][jet]) * data[i]['jet_mu_z0'][jet])
                    signed_d0 = abs(data[i]['jet_mu_d0'][jet]) * sign_d0
                    signed_z0 = abs(data[i]['jet_mu_z0'][jet]) * sign_z0

                    muonParentName = DefineParticle(int(abs(data[i]['jet_mu_parent_pdgid'][jet])))

                    #print muonParentName
                    if muonParentName not in ParentPdgId:
                        ParentPdgId[muonParentName] = {
                                                        "name":muonParentName,
                                                        "pdgId":int(abs(data[i]['jet_mu_parent_pdgid'][jet])),
                                                        "color":colorList[colorPlace],
                                                        "muon_pt":[data[i]['jet_mu_pt'][jet]/GeV],
                                                        "muon_smt":[data[i]['jet_mu_smt'][jet]],
                                                        "muon_deltar":[data[i]['jet_mu_dR'][jet]],
                                                        "muon_ptfrac":[data[i]['jet_mu_pt'][jet]/data[i]['jet_pt'][jet]],
                                                        "muon_ptrel":[data[i]['jet_mu_pTrel'][jet]/GeV],
                                                        "muon_dzero":[signed_d0],
                                                        "muon_zzero":[signed_z0],
                                                        "muon_qoverp":[data[i]['jet_mu_qOverPratio'][jet]*GeV]
                                                      }
                        colorPlace += 1
                    else:
                        ParentPdgId[muonParentName]["muon_pt"].append(data[i]['jet_mu_pt'][jet]/GeV)
                        ParentPdgId[muonParentName]["muon_smt"].append(data[i]['jet_mu_smt'][jet])
                        ParentPdgId[muonParentName]["muon_deltar"].append(data[i]['jet_mu_dR'][jet])
                        ParentPdgId[muonParentName]["muon_ptfrac"].append(data[i]['jet_mu_pt'][jet]/data[i]['jet_pt'][jet])
                        ParentPdgId[muonParentName]["muon_ptrel"].append(data[i]['jet_mu_pTrel'][jet]/GeV)
                        ParentPdgId[muonParentName]["muon_dzero"].append(signed_d0)
                        ParentPdgId[muonParentName]["muon_zzero"].append(signed_z0)
                        ParentPdgId[muonParentName]["muon_qoverp"].append(data[i]['jet_mu_qOverPratio'][jet]*GeV)

    for parentName in ParentPdgId:
        #give all our newly created histograms to the plots we initialized
        muon_pt_plot.appendHisto(ParentPdgId[parentName]["muon_pt"], ParentPdgId[parentName])
        muon_smt_plot.appendHisto(ParentPdgId[parentName]["muon_smt"], ParentPdgId[parentName])
        muon_deltar_plot.appendHisto(ParentPdgId[parentName]["muon_deltar"], ParentPdgId[parentName])
        muon_ptfrac_plot.appendHisto(ParentPdgId[parentName]["muon_ptfrac"], ParentPdgId[parentName])
        muon_ptrel_plot.appendHisto(ParentPdgId[parentName]["muon_ptrel"], ParentPdgId[parentName])
        muon_dzero_plot.appendHisto(ParentPdgId[parentName]["muon_dzero"], ParentPdgId[parentName])
        muon_zzero_plot.appendHisto(ParentPdgId[parentName]["muon_zzero"], ParentPdgId[parentName])
        muon_qoverp_plot.appendHisto(ParentPdgId[parentName]["muon_qoverp"], ParentPdgId[parentName])

    #add each new plot to the list of plots, which will be returned
    list_of_plots.append(muon_pt_plot)
    list_of_plots.append(muon_smt_plot)
    list_of_plots.append(muon_deltar_plot)
    list_of_plots.append(muon_ptfrac_plot)
    list_of_plots.append(muon_ptrel_plot)
    list_of_plots.append(muon_dzero_plot)
    list_of_plots.append(muon_zzero_plot)
    list_of_plots.append(muon_qoverp_plot)

    return list_of_plots

def printMuonPlots(plotList):
    for plot in plotList:
        plot.makePlot()
