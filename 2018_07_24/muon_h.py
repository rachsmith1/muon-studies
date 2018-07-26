from __future__ import division

import numpy as np
import pandas as pd
import scipy.stats as st

from numpy.lib.recfunctions import stack_arrays
from root_numpy import root2array, root2rec
import glob

from ROOT import TDatabasePDG
from ROOT import TParticlePDG

import matplotlib
import matplotlib.colors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
matplotlib.rcParams.update({'font.size': 16})
get_ipython().magic(u'matplotlib inline')

from collections import OrderedDict

GeV = 1000

JetType = OrderedDict()
JetType["bH"] = {"name":"b jets",               "pdgId":5,  "color":"blue"}
JetType["cH"] = {"name":"c jets",               "pdgId":4,  "color":"green"}
JetType["li"] = {"name":"light-flavoured jets", "pdgId":0,  "color":"red"}
JetType["tH"] = {"name":"$\\tau$ jets",         "pdgId":15, "color":"orange"}

class StackedPlot:
    def __init__(self, title, axisTitle, binning, normBool, logBool):
        #title of stacked plot
        self.title      = title
        #x-axis title of stacked plot
        self.axisTitle  = axisTitle

        #binning, i.e., max, min, and bin width of stacked plot
        self.binning    = binning
        #is the plot normalized?
        self.normBool   = normBool
        #is the y-axis log?
        self.logBool    = logBool

        #list of individual histograms that will be added to the stacked plot
        self.histoList  = []

    #append histograms to the list of histograms mentioned earlier
    def appendHisto(self,histoToAppend, histType):
        self.histoList.append([histoToAppend, histType])

    def makePlot(self):
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        #for the purposes of weighting
        ntotal = 0
        plotHistoList = []
        weightList = []
        colorList = []
        labelList = []
        for histo in self.histoList:
            if len(histo[0])==0: continue

            ntotal += len(histo[0])

            plotHistoList.append(histo[0])
            colorList.append(histo[1]["color"])
            labelList.append(histo[1]["name"])

        for histo in self.histoList:
            if len(histo[0])==0: continue

            weight=1.0
            #weight over the TOTAL # OF MUONS, i.e. all the muons from all of the jet types
            if self.normBool:
                weight = 1/ntotal
            weightsForHisto = [weight] * len(histo[0])
            weightList.append(weightsForHisto)

        plt.hist(
                    plotHistoList,
                    self.binning,
                    weights=weightList,
                    histtype='step',
                    stacked=False,
                    fill=False,
                    color=colorList,
                    label=labelList
                )


        #plot the legend
        plt.legend(bbox_to_anchor=(1.05, 0.52), loc=2, borderaxespad=0.)

        #plot the pt and eta bins for the plot
        plt.text(1.05, 1.00, "$N$ muons = {}".format(ntotal), transform=ax.transAxes)
        plt.text(1.05, 0.92, "jet $p_T$ > 20 GeV/c", transform=ax.transAxes)
        plt.text(1.05, 0.84, "jet |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.05, 0.76, "muon $p_T$ > 1 GeV/c", transform=ax.transAxes)
        plt.text(1.05, 0.68, "muon |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.05, 0.60, "Overlap Removal = True", transform=ax.transAxes)

        plt.title(self.title)
        plt.xlabel(self.axisTitle)
        if self.normBool:
            plt.ylabel("1/($N$ muons)")
        else:
            plt.ylabel("$N$")
        if self.logBool: plt.yscale('log')
        plt.tight_layout()
        plt.show()
