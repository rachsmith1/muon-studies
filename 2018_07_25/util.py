from __future__ import division

import numpy as np

import matplotlib
import matplotlib.colors
from matplotlib.colors import LogNorm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
matplotlib.rcParams.update({'font.size': 16})
get_ipython().magic(u'matplotlib inline')

from scipy.stats.stats import pearsonr

GeV = 1000

#This function takes in a pdgid and returns the name of the kind of particle it is associated with
def DefineParticle(pdgid):

    pdgid = abs(int(pdgid))

    if   pdgid==211: return "pi +/-"
    elif pdgid==999: return "pileup"
    elif pdgid==24:  return "W +/-"
    elif pdgid==15:  return "$\\tau$ +/-"
    elif pdgid==22:  return "photon"
    elif pdgid==321 or pdgid==130:
        return "strange meson"
    elif pdgid==221 or pdgid==223 or pdgid==333 or pdgid==113 or pdgid==331:
        return "light meson"
    elif np.floor(pdgid/1000)==5 or np.floor(pdgid/100)==5:
        return "b hadron"
    elif np.floor(pdgid/1000)==4 or np.floor(pdgid/100)==4:
        return "c hadron"
    else:
        return "N/A"

#compute the pearson correlation coefficient of two arrays
def PearsonCorrelationCoefficient(x,y):
    cov = 0
    for i,v in x.iteritems():
        cov += ((x[i] - np.mean(x))*(y[i] - np.mean(y)))
    cov = cov/len(x)

    return cov/(np.std(x) * np.std(y))

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

    def printPlot(self):
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        ntotal = 0
        for histo in self.histoList:
            if len(histo[0])==0: continue

            #count total entries
            ntotal += len(histo[0])

            #weight over each entry
            weight = 1.0
            if self.normBool: weight = 1/len(histo[0])
            weights = [weight] * len(histo[0])

            plt.hist(
                        histo[0],
                        self.binning,
                        weights=weights,
                        histtype='step',
                        fill=False,
                        alpha=1,
                        color=histo[1]["color"],
                        label=histo[1]["name"]
                    )

        #plot the legend
        plt.legend(bbox_to_anchor=(1.10, 0.52), loc=2, borderaxespad=0.)

        #plot the pt and eta bins for the plot
        plt.text(1.10, 1.00, "$N$ muons = {}".format(ntotal), transform=ax.transAxes)
        plt.text(1.10, 0.92, "jet $p_T$ > 20 GeV/c", transform=ax.transAxes)
        plt.text(1.10, 0.84, "jet |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.10, 0.76, "muon $p_T$ > 1 GeV/c", transform=ax.transAxes)
        plt.text(1.10, 0.68, "muon |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.10, 0.60, "Overlap Removal = True", transform=ax.transAxes)

        plt.title(self.title)
        plt.xlabel(self.axisTitle)
        if self.normBool:
            plt.ylabel("1/$N$")
        else:
            plt.ylabel("$N$")
        if self.logBool: plt.yscale('log')
        plt.tight_layout()
        plt.show()

class TwoDimensionalPlot:
    def __init__(self, title, xAxisTitle, yAxisTitle, xBinning, yBinning):
        #title of 2D plot
        self.title      = title
        #x-axis title of 2D plot
        self.xAxisTitle = xAxisTitle
        #y-axis title of 2D plot
        self.yAxisTitle = yAxisTitle

        #x-axis binning, i.e., max, min, and bin width of 2D plot
        self.xBinning    = xBinning
        #y-axis binning, i.e., max, min, and bin width of 2D plot
        self.yBinning    = yBinning

    #append histograms to the list of histograms mentioned earlier
    def appendHisto(self, xHisto, yHisto):
        #Histogram on x-axis
        self.xHisto = xHisto

        #Histogram on y-axis
        self.yHisto = yHisto

    def printPlot(self):
        fig = plt.figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        ntotal = len(self.xHisto)

        plt.hist2d(
                    self.xHisto,
                    self.yHisto,
                    bins = [self.xBinning, self.yBinning],
                    norm = LogNorm()
                   )

        #plot the pt and eta bins for the plot
        plt.text(1.25, 1.00, "$N$ muons = {}".format(ntotal), transform=ax.transAxes)
        plt.text(1.25, 0.92, "jet $p_T$ > 20 GeV/c", transform=ax.transAxes)
        plt.text(1.25, 0.84, "jet |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.25, 0.76, "muon $p_T$ > 1 GeV/c", transform=ax.transAxes)
        plt.text(1.25, 0.68, "muon |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.25, 0.60, "Overlap Removal = True", transform=ax.transAxes)
        plt.text(1.25, 0.52, "PCC = {}".format(round(pearsonr(self.xHisto, self.yHisto)[0], 5)), transform=ax.transAxes)
        plt.text(1.25, 0.44, "PCC $p$-value = {}".format(round(pearsonr(self.xHisto, self.yHisto)[1], 5)), transform=ax.transAxes)

        plt.title(self.title)
        plt.xlabel(self.xAxisTitle)
        plt.ylabel(self.yAxisTitle)
        plt.colorbar()
        plt.tight_layout()
        plt.show()

class BarPlot:
    def __init__(self, title):
        #Title of bar graph
        self.title = title

    def addData(self, data, labels):
        #Add data and labels to the bar graph
        self.data = data
        self.labels = labels

    def printPlot(self):
        fig = plt.figure(figsize=(5, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        plt.bar(
                    np.arange(len(self.data)),
                    self.data,
                    width=0.75,
                    color="rebeccapurple"
        )

        #plot the numerical values for each bar on top of bar
        ntotal = 0
        for i, v in enumerate(self.data):
            ntotal += v
        for i, v in enumerate(self.data):
            plt.text(i - .25, ntotal*0.02, str(v), color="white")

        #plot the pt and eta bins for the plot
        plt.text(1.10, 1.00, "$N$ muons = {}".format(ntotal), transform=ax.transAxes)
        plt.text(1.10, 0.92, "jet $p_T$ > 20 GeV/c", transform=ax.transAxes)
        plt.text(1.10, 0.84, "jet |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.10, 0.76, "muon $p_T$ > 1 GeV/c", transform=ax.transAxes)
        plt.text(1.10, 0.68, "muon |$\eta$| < 2.5", transform=ax.transAxes)
        plt.text(1.10, 0.60, "Overlap Removal = True", transform=ax.transAxes)

        plt.title(self.title)
        plt.ylabel("$N$")
        plt.xticks(np.arange(len(self.data)), self.labels, rotation=30)
        plt.tight_layout()
        plt.show()
