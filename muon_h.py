
# coding: utf-8

# In[1]:

#!/usr/bin/env python
from __future__ import division


# In[2]:

import numpy as np
import pandas as pd
import scipy.stats as st

from numpy.lib.recfunctions import stack_arrays
from root_numpy import root2array, root2rec
import glob


# In[3]:

import matplotlib
import matplotlib.colors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
matplotlib.rcParams.update({'font.size': 16})
get_ipython().magic(u'matplotlib inline')


# In[4]:

from collections import OrderedDict


# In[5]:

GeV = 1000


# In[6]:

JetType = OrderedDict()
JetType["bH"] = {"name":"b jets",               "pdgId":5, "color":"blue"}
JetType["cH"] = {"name":"c jets",               "pdgId":4, "color":"green"}
JetType["li"] = {"name":"light-flavoured jets", "pdgId":0, "color":"red"}
JetType["tH"] = {"name":"$\\tau$ jets",             "pdgId":15,"color":"yellow"}


# In[7]:

PtBins = OrderedDict()
PtBins["20_50"]   = {"name":"jet $p_T$: 20-50 GeV","min":20,"max":50}
PtBins["50_100"]  = {"name":"jet $p_T$: 50-100 GeV","min":50,"max":100}
PtBins["100_200"] = {"name":"jet $p_T$: 100-200 GeV","min":100,"max":200}
PtBins["200_500"] = {"name":"jet $p_T$: 200-500 GeV","min":200,"max":500}


# In[8]:

EtaBins = OrderedDict()
EtaBins["0_1"]   = {"name":"$0 \leq jet |\eta| < 1$","min":0,"max":1} 
EtaBins["1_2.5"] = {"name":"$1 \leq jet |\eta| < 2.5$","min":1,"max":2.5}


# In[9]:

#Not currently using. I used this class initially to test out the individual jet type plots.

class UnstackedPlot:
    def __init__(self, title, axisTitle, data, binning, normBool, logBool, jetType, ptBin, etaBin):
        self.title     = title
        self.axisTitle = axisTitle
        
        self.data      = data
        self.binning   = binning
        self.normBool  = normBool
        self.logBool   = logBool
        
        self.jetType   = jetType
        self.ptBin     = ptBin
        self.etaBin    = etaBin
        
    def makePlot(self):
        fig = plt.figure(figsize=(5, 3.5), dpi=100)
        ax = fig.add_subplot(111)
        
        if len(self.data)==0: self.normBool = False
        
        plt.hist(self.data, self.binning, normed = self.normBool, histtype='step', fill=False, color=self.jetType["color"])
        
        plt.text(1.05, 0.95, self.jetType["name"], transform=ax.transAxes)
        plt.text(1.05, 0.85, self.ptBin["name"], transform=ax.transAxes)
        plt.text(1.05, 0.75, self.etaBin["name"], transform=ax.transAxes)
        plt.text(1.05, 0.65, "N = {0}".format(len(self.data)), transform=ax.transAxes)
            
        plt.title(self.title)    
        plt.xlabel(self.axisTitle)
        plt.ylabel("1/N")
        if self.logBool and len(self.data)!=0: plt.yscale('log')
        plt.tight_layout()
        plt.show()


# In[10]:

class StackedPlot:
    def __init__(self, title, axisTitle, binning, normBool, logBool, ptBin, etaBin):
        #title of stacked plot
        self.title     = title
        #x-axis title of stacked plot
        self.axisTitle = axisTitle
        
        #binning, i.e., max, min, and bin width of stacked plot
        self.binning   = binning
        #is the plot normalized?
        self.normBool  = normBool
        #is the y-axis log?
        self.logBool   = logBool
        
        #what pt-bin is the plot?
        self.ptBin     = ptBin
        #what eta-bin is the plot?
        self.etaBin    = etaBin
        
        #list of individual histograms that will be added to the stacked plot
        self.histoList = []
    
    #append histograms to the list of histograms mentioned earlier
    def appendHisto(self,histoToAppend, jetType):
        self.histoList.append([histoToAppend, jetType])
        
    def makePlot(self):
        fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        #for the purposes of weighting
        ntotal = 0
        for histo in self.histoList:
            ntotal += len(histo[0])
                    
        for histo in self.histoList:
            #check for empty histograms
            if len(histo[0])==0: continue
            
            weight=1.0
            #weight over the TOTAL # OF MUONS, i.e. all the muons from all of the jet types
            if self.normBool: 
                weight = 1/ntotal
            weight_list = [weight] * len(histo[0])
            
            plt.hist(histo[0], self.binning, weights=weight_list, histtype='step', fill=False, color=histo[1]["color"], label=histo[1]["name"])
        
        #plot the legend
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        #plot the pt and eta bins for the plot
        plt.text(1.05, 0.55, self.ptBin["name"], transform=ax.transAxes)
        plt.text(1.05, 0.45, self.etaBin["name"], transform=ax.transAxes)
                
        plt.title(self.title)    
        plt.xlabel(self.axisTitle)
        if self.normBool: 
            plt.ylabel("1/($N$ muons)")
        else:
            plt.ylabel("$N$")            
        if self.logBool: plt.yscale('log')
        plt.tight_layout()
        plt.show()       

