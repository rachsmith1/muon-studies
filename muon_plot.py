from muon_h import *

def makeMuonPlots(data, jpb, jeb, mpb, meb):

    #initialize all the plots we're going to make for each pt bin and eta bin
    muon_pt_plot     = StackedPlot("Muon $p_T$",
                                  "$p_T$ [GeV/c]",
                                  np.linspace(0,450,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_deltar_plot = StackedPlot("$\Delta R$($\mu$,jet)",
                                  "$\Delta R$",
                                  np.linspace(0,0.5,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_ptfrac_plot = StackedPlot("${p_T}^{\mu} / {p_T}^{jet}$",
                                  "${p_T}^{\mu} / {p_T}^{jet}$",
                                  np.linspace(0,2,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_dzero_plot  = StackedPlot("Muon $d_0$",
                                  "$d_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_zzero_plot  = StackedPlot("Muon $z_0$",
                                  "$z_0$ [mm]",
                                  np.linspace(-6,6,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_dsig_plot   = StackedPlot("Muon $d_0 / \sigma_{d_0}$",
                                  "$d_0 / \sigma_{d_0}$",
                                  np.linspace(0,0.6,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    muon_zsig_plot   = StackedPlot("Muon $z_0 / \sigma_{z_0}$",
                                  "$z_0 / \sigma_{z_0}$",
                                  np.linspace(0,0.6,50),
                                  True,
                                  True,
                                  jpb,
                                  jeb,
                                  mpb,
                                  meb)

    #now loop over each type of jet
    for jt in JetType:

        #we will fill these lists with the corresponding data for the selected jet type
        muon_pt     = []
        muon_deltar = []
        muon_ptfrac = []
        muon_dzero  = []
        muon_zzero  = []
        muon_dsig   = []
        muon_zsig   = []

        #for each event in the dataset
        for i in range(data.size):
            #for each jet in that event
            for jet in range(data[i]['jet_pt'].size):
                #cut on the jet pt bin, the jet eta bin, and the jet type
                if (
                    data[i]['jet_pt'][jet] >= jpb[0]*GeV and
                    data[i]['jet_pt'][jet] <  jpb[1]*GeV and

                    abs(data[i]['jet_eta'][jet]) >= jeb[0] and
                    abs(data[i]['jet_eta'][jet]) <  jeb[1] and

                    data[i]['jet_LabDr_HadF'][jet] == JetType[jt]["pdgId"]
                   ):
                    #for each associated track in that jet
                    for trk in range(data[i]['jet_trk_pt'][jet].size):
                        #check if that track is matched with a muon
                        #and cut on the muon pt bin and muon eta bin
                        if (
                            abs(data[i]['jet_trk_pdg_id'][jet][trk])==13 and

                            data[i]['jet_trk_pt'][jet][trk] >= mpb[0]*GeV and
                            data[i]['jet_trk_pt'][jet][trk] <  mpb[1]*GeV and

                            abs(data[i]['jet_trk_eta'][jet][trk]) >= meb[0] and
                            abs(data[i]['jet_trk_eta'][jet][trk]) <  meb[1]
                           ):

                            #append all the relevant data to the lists we made earlier
                            muon_pt.append(data[i]['jet_trk_pt'][jet][trk]/GeV)

                            deta = data[i]['jet_eta'][jet] - data[i]['jet_trk_eta'][jet][trk]
                            dphi = data[i]['jet_phi'][jet] - data[i]['jet_trk_phi'][jet][trk]
                            muon_deltar.append(np.sqrt(deta*deta + dphi*dphi))

                            muon_ptfrac.append(data[i]['jet_trk_pt'][jet][trk]/data[i]['jet_pt'][jet])

                            muon_dzero.append(data[i]['jet_trk_ip3d_d0'][jet][trk])

                            muon_zzero.append(data[i]['jet_trk_ip3d_z0'][jet][trk])

                            muon_dsig.append(data[i]['jet_trk_ip3d_d0'][jet][trk]/data[i]['jet_trk_ip3d_d0sig'][jet][trk])

                            muon_zsig.append(data[i]['jet_trk_ip3d_z0'][jet][trk]/data[i]['jet_trk_ip3d_z0sig'][jet][trk])

        #give all our newly created histograms to the plots we initialized
        muon_pt_plot.appendHisto(muon_pt, JetType[jt])
        muon_deltar_plot.appendHisto(muon_deltar, JetType[jt])
        muon_ptfrac_plot.appendHisto(muon_ptfrac, JetType[jt])
        muon_dzero_plot.appendHisto(muon_dzero, JetType[jt])
        muon_zzero_plot.appendHisto(muon_dzero, JetType[jt])
        muon_dsig_plot.appendHisto(muon_dsig, JetType[jt])
        muon_zsig_plot.appendHisto(muon_zsig, JetType[jt])

    #print the plots
    muon_pt_plot.makePlot()
    muon_deltar_plot.makePlot()
    muon_ptfrac_plot.makePlot()
    muon_dzero_plot.makePlot()
    muon_zzero_plot.makePlot()
    muon_dsig_plot.makePlot()
    muon_zsig_plot.makePlot()
